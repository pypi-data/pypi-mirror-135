import logging
from email.errors import MessageDefect, MessageParseError
from email.headerregistry import Address
from functools import reduce
from pathlib import Path
from typing import Any, Optional, Union

import limits.storage
import limits.strategies
import ruteni.apis.logging
import ruteni.plugins.translation
from pkg_resources import resource_filename
from ruteni.apis.security import get_security_headers
from ruteni.apis.users import get_user_by_email
from ruteni.apps import LocalizedAppNode
from ruteni.config import config
from ruteni.plugins.locale import locales
from ruteni.plugins.passwords import register_user
from ruteni.plugins.session import get_user_from_environ
from ruteni.plugins.socketio import sio
from ruteni.plugins.verifications import EmailVerifier
from ruteni.routing import current_path_in
from ruteni.routing.nodes.http.file import FileNode
from ruteni.services.database import database
from ruteni.utils.dns import RecordList, query_mx
from sqlalchemy.sql import select
from transitions.core import MachineError
from transitions.extensions.asyncio import AsyncMachine
from zxcvbn import zxcvbn

logger = logging.getLogger(__name__)

Issues = dict[str, Union[bool, int, str]]

MINIMUM_PASSWORD_STRENGTH: int = config.get(
    "RUTENI_REGISTRATION_MINIMUM_PASSWORD_STRENGTH", cast=int, default=3
)
MAXIMUM_DISPLAY_NAME_LENGTH: int = config.get(
    "RUTENI_REGISTRATION_MAXIMUM_DISPLAY_NAME_LENGTH", cast=int, default=40
)
MAXIMUM_EMAIL_LENGTH: int = config.get(
    "RUTENI_REGISTRATION_MAXIMUM_EMAIL_LENGTH", cast=int, default=40
)
MAXIMUM_PASSWORD_LENGTH: int = config.get(
    "RUTENI_REGISTRATION_MAXIMUM_PASSWORD_LENGTH", cast=int, default=40
)
NAMESPACE = config.get("RUTENI_REGISTRATION_NAMESPACE", default="/ruteni/registration")

KNOWN_LOCALES = ("en-EN", "fr-FR")  # TODO: from available emails

# https://limits.readthedocs.org
# https://haliphax.dev/2021/03/rate-limiting-with-flask-socketio/
# https://pypi.org/project/fastapi-limiter/

# uri = "redis+unix:///var/run/redis/redis-server.sock"
# options: dict = {}
# redis_storage = limits.storage.storage_from_string(uri, **options)
memory_storage = limits.storage.MemoryStorage()
one_per_second = limits.RateLimitItemPerSecond(1, 1)
moving_window = limits.strategies.MovingWindowRateLimiter(memory_storage)


class Registration:
    """User registration."""

    def __init__(self) -> None:
        self.display_name: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.locale: Optional[str] = None
        self.records: Optional[RecordList] = None
        self.email_verifier: Optional[EmailVerifier] = None
        self.issues: dict[str, Issues] = dict(
            display_name={}, email={}, password={}, locale={}
        )

    async def input_ok(
        self, rv: list, *, display_name: str, email: str, password: str, locale: str
    ) -> bool:
        """Set the registration information."""
        if self.display_name != display_name:
            issues = self.issues["display_name"]
            issues.clear()
            if display_name == "":
                issues["invalid-display-name"] = "empty"
            elif len(display_name) > MAXIMUM_DISPLAY_NAME_LENGTH:
                issues["invalid-display-name"] = "overflow"
            self.display_name = display_name

        if self.email != email:
            issues = self.issues["email"]
            issues.clear()
            if len(email) == 0:
                issues["invalid-email"] = "empty"
            elif len(email) > MAXIMUM_EMAIL_LENGTH:
                issues["invalid-email"] = "overflow"
            elif "@" not in email or (
                len(email) > 1 and email[-1] == "@" and "@" not in email[:-1]
            ):
                # input is something like `foo` or 'foo@'
                try:
                    email.encode("ascii")
                except UnicodeEncodeError:
                    issues["invalid-email"] = "parse-error"
                else:
                    issues["invalid-email"] = "incomplete"
            else:
                try:
                    address = Address(display_name=display_name, addr_spec=email)
                except (IndexError, MessageDefect, MessageParseError):
                    issues["invalid-email"] = "parse-error"
                else:
                    logger.debug(f"resolving MX for {address.domain}")
                    records = await query_mx(address.domain)
                    if records is None:
                        issues["invalid-email"] = "unknown-domain"
                    else:
                        logger.debug(f"found records: {records}")
                        if len(records):
                            self.records = sorted(records, key=lambda rec: rec.priority)
                        else:
                            issues["invalid-email"] = "misconfigured-domain"
            self.email = email

        if self.password != password:
            issues = self.issues["password"]
            issues.clear()
            if len(password) == 0:
                issues["invalid-password"] = "empty"
            elif len(password) > MAXIMUM_EMAIL_LENGTH:
                issues["invalid-password"] = "overflow"
            else:
                results = zxcvbn(password, user_inputs=[display_name, email])
                if results["score"] < MINIMUM_PASSWORD_STRENGTH:
                    issues["low-password-strength"] = results["score"]
            self.password = password

        if self.locale != locale:
            issues = self.issues["locale"]
            issues.clear()
            if locale == "":
                issues["invalid-locale"] = "empty"
            else:
                locale_id = await database.fetch_val(
                    select([locales.c.id]).where(locales.c.code == locale)
                )
                if locale_id is None:
                    issues["invalid-locale"] = "unknown"
            self.locale = locale

        issues = reduce(lambda a, b: {**a, **b}, self.issues.values())
        rv.append(issues)
        return len(issues) == 0

    async def sent_ok(self, rv: list) -> int:
        assert self.display_name and self.email and self.records

        # ignore registration if an active user with the same email exists
        user_info = await get_user_by_email(self.email)
        if user_info is not None:
            # TODO: do everything but send the email to protect users' privacy? by
            # timing a failed registration, one could deduce that a user has an account
            rv.append(False)
            return False

        template_path = Path(
            resource_filename(__name__, f"emails/{self.locale}/verification.html")
        )

        self.email_verifier = EmailVerifier()
        sent = await self.email_verifier.send_verification_code(
            self.display_name, self.email, self.records, template_path
        )
        rv.append(sent)
        return sent

    async def expired(self, rv: list, code: str) -> bool:
        assert self.email_verifier
        expired = self.email_verifier.code_expired()
        if expired:
            rv.append(-1)
        return expired

    async def too_many(self, rv: list, code: str) -> bool:
        assert self.email_verifier
        remaining_attempts = self.email_verifier.incr_attempts()
        rv.append(remaining_attempts)
        return remaining_attempts == 0

    async def code_ok(self, rv: list, code: str) -> bool:
        assert self.email_verifier
        correct = self.email_verifier.code_correct(code)
        logger.debug("code_ok?", correct)

        if correct:
            assert self.display_name and self.email and self.locale and self.password
            user_id, password_id = await register_user(
                self.display_name, self.email, self.locale, self.password
            )
            await self.email_verifier.user_verified(user_id)
            logger.debug(
                "account created:", user_id, self.display_name, self.email, password_id
            )

            # logger.debug(await group_manager.add_user_to_group(user_id, "admin"))

        # TODO: send error type (code incorrect or expired)
        if correct:
            rv.append(None)
        return correct


nodes = (
    FileNode(
        current_path_in(("", "/index.html")),
        resource_filename(__name__, "resources/index.html"),
        headers=get_security_headers(script=True, connect=True, style=True, img=True),
        media_type="text/html",
    ),
)


app_node = LocalizedAppNode("registration", 1, nodes, ("fr-FR", "en-US"), {database})

TRANSITIONS = (
    {"trigger": "edit", "source": "Bad", "dest": "Good", "conditions": "input_ok"},
    {"trigger": "edit", "source": "Bad", "dest": "Bad"},
    {"trigger": "edit", "source": "Good", "dest": "Good", "conditions": "input_ok"},
    {"trigger": "edit", "source": "Good", "dest": "Bad"},
    {"trigger": "register", "source": "Good", "dest": "Sent", "conditions": "sent_ok"},
    {"trigger": "register", "source": "Good", "dest": "Good"},
    {"trigger": "modify", "source": "Sent", "dest": "Good"},
    {"trigger": "retry", "source": "Sent", "dest": "Sent"},
    {"trigger": "verify", "source": "Sent", "dest": "Good", "conditions": "expired"},
    {"trigger": "verify", "source": "Sent", "dest": "Done", "conditions": "code_ok"},
    {"trigger": "verify", "source": "Sent", "dest": "Good", "conditions": "too_many"},
    {"trigger": "verify", "source": "Sent", "dest": "Sent"},
    {"trigger": "disconnect", "source": "*", "dest": "Disconnected"},
)
TRIGGERS = set(transition["trigger"] for transition in TRANSITIONS)
REGISTRATION_FSM = {
    "states": ("Bad", "Good", "Sent", "Done", "Disconnected"),
    "initial": "Bad",
    "transitions": TRANSITIONS,
}


machines: dict[str, AsyncMachine] = {}


def on_connect(sid: str, environ: dict[str, str]) -> bool:
    # if the user is connected, reject connection
    if get_user_from_environ(environ) is not None:
        return False

    registration = Registration()
    machines[sid] = AsyncMachine(registration, **REGISTRATION_FSM)
    logger.debug(f"{sid} connected")
    return True


async def on_disconnect(sid: str) -> None:
    await machines[sid].model.disconnect()
    del machines[sid]
    logger.debug(f"{sid} disconnected")


async def catch_all(event: str, sid: str, data: Optional[Any] = None) -> Any:
    logger.debug(event, machines[sid].model.state, data)
    if event not in TRIGGERS:
        return {"error": "unknown-command"}
    rv: list = []
    registration = machines[sid].model
    try:
        if data is None:
            await registration.trigger(event, rv)
        elif isinstance(data, dict):
            await registration.trigger(event, rv, **data)
        elif isinstance(data, list):
            await registration.trigger(event, rv, *data)
        else:
            await registration.trigger(event, rv, data)
    except MachineError:
        return {"error": "unauthorized-command"}
    except TypeError:
        # this exception will be raised if the command parameters are wrong, e.g.:
        #   input_ok() got an unexpected keyword argument 'invalid-display-name'
        # TODO: this exception is too broad
        return {"error": "invalid-arguments"}
    except Exception:
        logger.exception("unexpected")
        return {"error": "unexpected-error"}

    logger.debug("rv", rv)
    return tuple(rv)


# TODO: use socketio.AsyncNamespace if there is a solution for catch-all
sio.on("connect", on_connect, namespace=NAMESPACE)
sio.on("disconnect", on_disconnect, namespace=NAMESPACE)
sio.on("*", catch_all, namespace=NAMESPACE)
