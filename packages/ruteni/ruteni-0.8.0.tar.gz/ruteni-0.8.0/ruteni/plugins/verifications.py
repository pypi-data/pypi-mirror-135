import logging
import quopri
from datetime import datetime, timedelta
from email import message_from_string
from email.utils import formataddr
from pathlib import Path
from random import randint

from ruteni.apis.users import users
from ruteni.config import config
from ruteni.plugins.site import ABUSE_URL, SITE_NAME
from ruteni.plugins.sqlalchemy import metadata
from ruteni.services.database import database
from ruteni.utils.dns import RecordList
from ruteni.utils.jinja2 import get_template_from_path
from ruteni.utils.smtp import send_mail

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, func

logger = logging.getLogger(__name__)

FROM_ADDRESS: str = config.get("RUTENI_VERIFICATION_FROM_ADDRESS")
VERIFICATION_CODE_LENGTH: int = config.get(
    "RUTENI_VERIFICATION_CODE_LENGTH", cast=int, default=6
)
VERIFICATION_CODE_EXPIRATION_MINUTES: int = config.get(
    "RUTENI_VERIFICATION_CODE_EXPIRATION_MINUTES", cast=int, default=1  # 20 minutes
)
VERIFICATION_MAX_ATTEMPTS: int = config.get(
    "RUTENI_VERIFICATION_MAX_ATTEMPTS", cast=int, default=3
)

verifications = Table(
    "verifications",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("sent_at", DateTime, nullable=False),
    Column("verified_at", DateTime, nullable=False, server_default=func.now()),
)


class EmailVerifier:
    async def send_verification_code(
        self,
        display_name: str,
        email: str,
        records: RecordList,
        template_path: Path,
    ) -> int:
        random_code = randint(0, 10 ** VERIFICATION_CODE_LENGTH - 1)
        self.verification_code = f"{{:0{VERIFICATION_CODE_LENGTH}}}".format(random_code)
        self.attempts = 0

        logger.debug(f"email template: {template_path}")
        params = {
            "email": email,
            "from": FROM_ADDRESS,
            "to": formataddr((display_name, email)),
            "display_name": display_name,
            "site_name": SITE_NAME,
            "verification_code": self.verification_code,
            "abuse_url": ABUSE_URL,
        }
        template = await get_template_from_path(template_path)
        content = await template.render_async(params)
        message = message_from_string(
            quopri.encodestring(content.encode("utf-8")).decode("utf-8")
        )
        logger.debug(message)
        # self.sent_at = datetime.now()
        # return VERIFICATION_CODE_EXPIRATION_MINUTES

        for record in records:
            success = await send_mail(message, record.host)
            if success:
                self.sent_at = datetime.now()
                return VERIFICATION_CODE_EXPIRATION_MINUTES

        # SMTPConnectError: 421 Your IP (82.66.70.213) is temporary blacklisted by an
        # anti-troyan rule, retry later and/or visit http://postmaster.free.fr/
        # https://forum.ubuntu-fr.org/viewtopic.php?id=2008675
        logger.warn("could not deliver email")
        return 0

    def incr_attempts(self) -> int:
        self.attempts += 1
        return VERIFICATION_MAX_ATTEMPTS - self.attempts

    def code_expired(self) -> bool:
        return datetime.now() - self.sent_at > timedelta(
            minutes=VERIFICATION_CODE_EXPIRATION_MINUTES
        )

    def code_correct(self, code: str) -> bool:
        return self.verification_code == code

    async def user_verified(self, user_id: int) -> int:
        return await database.execute(
            verifications.insert().values(user_id=user_id, sent_at=self.sent_at)
        )
