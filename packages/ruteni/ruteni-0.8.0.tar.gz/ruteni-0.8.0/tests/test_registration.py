import os
from html.parser import HTMLParser
from typing import Any
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import socketio

from .config import (
    BASE_URL,
    DOMAIN,
    USER_EMAIL,
    USER_LOCALE,
    USER_NAME,
    USER_PASSWORD,
    clear_database,
    test_env,
)

with patch.dict(os.environ, test_env):
    from ruteni.app import Ruteni
    from ruteni.apps.registration import NAMESPACE
    from ruteni.plugins.verifications import VERIFICATION_MAX_ATTEMPTS

from ruteni.routing import current_path_is
from ruteni.routing.nodes.http import load_http_node_entry_point
from ruteni.routing.nodes.websocket import WebSocketEntryPointNode

from .dns import DNSMock
from .server import UvicornTestServer
from .smtp import SMTPMock

MX_SERVER = "mx." + DOMAIN


class VerificationEmailHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_a = False
        self.code: str = ""

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if self.code == "":
            self.in_a = tag == "a"

    def handle_endtag(self, tag: str) -> None:
        if self.code == "":
            self.in_a = False

    def handle_data(self, data: str) -> None:
        if self.code == "" and self.in_a and len(data) == 6:
            self.code = data


class RegistrationTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.server = UvicornTestServer(
            Ruteni(
                http_node=load_http_node_entry_point("ruteni", "register"),
                websocket_node=WebSocketEntryPointNode(
                    current_path_is("/socket.io/"), "ruteni", "socketio"
                ),
                services={"ruteni:database"},
            )
        )
        await self.server.up()
        self.sio = socketio.AsyncClient(reconnection=False)
        await self.sio.connect(BASE_URL, transports=["websocket"], namespaces=NAMESPACE)

    async def asyncTearDown(self) -> None:
        await self.sio.disconnect()
        await self.sio.eio.http.close()  # TODO: socketio bug?
        await self.server.down()

    def tearDown(self) -> None:
        clear_database()

    async def call(self, *args, **kwargs) -> Any:  # type: ignore
        return await self.sio.call(*args, namespace=NAMESPACE, **kwargs)

    async def emit_edit(
        self, display_name: str, email: str, password: str, locale: str
    ) -> dict:
        return await self.call(
            "edit",
            {
                "display_name": display_name,
                "email": email,
                "password": password,
                "locale": locale,
            },
        )

    async def test_register(self) -> None:
        # send a bogus event
        self.assertEqual(await self.call("unknown"), {"error": "unknown-command"})

        # send bogus arguments
        self.assertEqual(await self.call("edit", None), {"error": "invalid-arguments"})
        self.assertEqual(await self.call("edit", 42), {"error": "invalid-arguments"})
        self.assertEqual(await self.call("edit", "a"), {"error": "invalid-arguments"})
        self.assertEqual(await self.call("edit", []), {"error": "invalid-arguments"})
        self.assertEqual(await self.call("edit", {}), {"error": "invalid-arguments"})
        self.assertEqual(
            await self.call("edit", {"email": ""}), {"error": "invalid-arguments"}
        )
        self.assertEqual(
            await self.call("edit", {"bogus-param": ""}), {"error": "invalid-arguments"}
        )

        self.assertEqual(
            await self.emit_edit("", "", "", ""),
            {
                "invalid-display-name": "empty",
                "invalid-email": "empty",
                "invalid-password": "empty",
                "invalid-locale": "empty",
            },
        )
        self.assertEqual(
            await self.emit_edit(100 * "x", 100 * "x", 100 * "x", ""),
            {
                "invalid-display-name": "overflow",
                "invalid-email": "overflow",
                "invalid-password": "overflow",
                "invalid-locale": "empty",
            },
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "incomplete-email", "", USER_LOCALE),
            {"invalid-email": "incomplete", "invalid-password": "empty"},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "foo@", "", "en-US"),
            {"invalid-email": "incomplete", "invalid-password": "empty"},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "fooé@", "", "de-DE"),
            {
                "invalid-email": "parse-error",
                "invalid-password": "empty",
                "invalid-locale": "unknown",
            },
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "@", "", USER_LOCALE),
            {"invalid-email": "parse-error", "invalid-password": "empty"},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "@fr", "", USER_LOCALE),
            {"invalid-email": "parse-error", "invalid-password": "empty"},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "foo@@", "bad", USER_LOCALE),
            {"invalid-email": "parse-error", "low-password-strength": 0},
        )
        self.assertEqual(
            await self.emit_edit(USER_NAME, "é@bar", "littlebetter", USER_LOCALE),
            {"invalid-email": "parse-error", "low-password-strength": 1},
        )

        dns = DNSMock({DOMAIN: [(MX_SERVER, 1, 1)]})
        with patch(
            "ruteni.apps.registration.query_mx",
            wraps=dns.query_mx,
        ):
            self.assertEqual(
                await self.emit_edit(USER_NAME, "foo@é", "0xbar45", USER_LOCALE),
                {"invalid-email": "unknown-domain", "low-password-strength": 2},
            )

        with patch(
            "ruteni.apps.registration.query_mx",
            wraps=dns.query_mx,
        ):
            self.assertEqual(
                await self.emit_edit(USER_NAME, USER_EMAIL, USER_PASSWORD, USER_LOCALE),
                {},
            )

        # now that the fields are okay, register using a mock SMTP function
        smtp = SMTPMock()
        with patch(
            "ruteni.plugins.verifications.send_mail",
            wraps=smtp.send_mail,
        ):
            self.assertTrue(await self.call("register"))

        # send a wrong verification code
        self.assertEqual(
            await self.call("verify", "xxxxxx"), VERIFICATION_MAX_ATTEMPTS - 1
        )
        self.assertEqual(
            await self.call("verify", "xxxxxx"), VERIFICATION_MAX_ATTEMPTS - 2
        )

        # get the email that was sent, extract the code and send it
        message = smtp.get_email(MX_SERVER)
        html = message.get_payload()
        parser = VerificationEmailHTMLParser()
        parser.feed(html)
        self.assertEqual(await self.call("verify", parser.code), None)

        # send a known event but in the wrong state
        self.assertEqual(await self.call("edit"), {"error": "unauthorized-command"})


if __name__ == "__main__":
    import unittest

    unittest.main()
