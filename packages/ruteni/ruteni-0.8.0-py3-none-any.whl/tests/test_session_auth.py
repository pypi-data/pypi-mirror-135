import asyncio
import os
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from ruteni import status
from ruteni.apis import api_nodes
from ruteni.app import Ruteni
from ruteni.routing.extractors import PrefixExtractor
from ruteni.routing.nodes import ExtractorNode, IterableNode
from ruteni.routing.nodes.http import ALL_METHODS
from starlette.testclient import TestClient

from .config import (
    BASE_URL,
    CLIENT_ID,
    USER,
    USER_EMAIL,
    USER_LOCALE,
    USER_NAME,
    USER_PASSWORD,
    clear_database,
    test_env,
)

with patch.dict(os.environ, test_env):
    from ruteni.plugins.passwords import register_user
    from ruteni.plugins.session import get_user_from_session

SIGNIN_URL = BASE_URL + "/api/auth/v1/signin"
SIGNOUT_URL = BASE_URL + "/api/auth/v1/signout"
USER_INFO_URL = BASE_URL + "/api/user/v1/info"


class SessionAuthTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.ruteni = Ruteni(
            ExtractorNode(PrefixExtractor("/api"), IterableNode(api_nodes)),
            services={"ruteni:auth-api", "ruteni:user-api"},
        )

    def tearDown(self) -> None:
        clear_database()

    def test_login(self) -> None:
        with TestClient(self.ruteni) as client:
            asyncio.run(
                register_user(USER_NAME, USER_EMAIL, USER_LOCALE, USER_PASSWORD)
            )

            # signin with wrong methods
            for method in ALL_METHODS:
                if method != "POST":
                    response = client.request(method, SIGNIN_URL)
                    self.assertEqual(
                        response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                    )

            # signin with bad parameters
            response = client.post(
                SIGNIN_URL, json={"email": "", "password": "", "client_id": ""}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            # signin with an unknown email
            response = client.post(
                SIGNIN_URL,
                json={"email": "foo@bar.fr", "password": "", "client_id": CLIENT_ID},
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            # signin with a bad password
            response = client.post(
                SIGNIN_URL,
                json={
                    "email": USER_EMAIL,
                    "password": "bad-password",
                    "client_id": CLIENT_ID,
                },
            )
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            # signin with correct credentials
            response = client.post(
                SIGNIN_URL,
                json={
                    "email": USER_EMAIL,
                    "password": USER_PASSWORD,
                    "client_id": CLIENT_ID,
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), USER)
            self.assertEqual(get_user_from_session(client.cookies["session"]), USER)

            # get user info when authenticated
            response = client.get(USER_INFO_URL)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), USER)

            # signout
            for method in ALL_METHODS:
                if method not in ("GET", "HEAD"):
                    response = client.request(method, SIGNOUT_URL)
                    self.assertEqual(
                        response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                    )

            response = client.get(SIGNOUT_URL)
            self.assertEqual(client.cookies.get_dict(), {})

            # get user info when not authenticated
            response = client.get(USER_INFO_URL)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


if __name__ == "__main__":
    import unittest

    unittest.main()
