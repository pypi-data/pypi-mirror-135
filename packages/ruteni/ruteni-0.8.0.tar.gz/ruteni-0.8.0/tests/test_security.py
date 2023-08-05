import os
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from ruteni.apis import api_nodes
from ruteni.app import Ruteni
from ruteni.routing.extractors import PrefixExtractor
from ruteni.routing.nodes import ExtractorNode, IterableNode
from ruteni.routing.nodes.http import ALL_METHODS
from sqlalchemy.sql import select
from starlette import status
from starlette.testclient import TestClient

from .config import clear_database, test_env

with patch.dict(os.environ, test_env):
    from ruteni.apis.security import (
        CSP_REPORT_CONTENT_TYPE,
        CSP_REPORT_KEY,
        EXPECT_CT_CONTENT_TYPE,
        EXPECT_CT_KEY,
        ReportType,
        security_reports,
    )
    from ruteni.services.database import database

CSP_REPORT_URI = "/api/security/v1/csp-report"
EXPECT_CT_URI = "/api/security/v1/expect-ct"

CSP_REPORT = {
    "csp-report": {
        "document-uri": "http://localhost:8000/app/store/",
        "referrer": "",
        "violated-directive": "script-src-elem",
        "effective-directive": "script-src-elem",
        "original-policy": "default-src 'self'; worker-src 'self'; frame-src 'none'; child-src 'none'; object-src 'none'; require-trusted-types-for 'script'; report-uri /api/logging/v1/csp-report/;",
        "disposition": "enforce",
        "blocked-uri": "inline",
        "line-number": 16,
        "source-file": "http://localhost:8000/app/store/",
        "status-code": 200,
        "script-sample": "",
    }
}
EXPECT_CT_REPORT = {
    "expect-ct-report": {
        "date-time": "2017-05-05T12:45:00Z",
        "hostname": "example.com",
        "port": 443,
        "effective-expiration-date": "2017-05-05T12:45:00Z",
        "foo": "bar",
    }
}


class SecurityTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.ruteni = Ruteni(
            ExtractorNode(PrefixExtractor("/api"), IterableNode(api_nodes)),
            services={"ruteni:security-api"},
        )

    def tearDown(self) -> None:
        clear_database()

    async def test_csp_report(self) -> None:
        with TestClient(self.ruteni) as client:
            for method in ALL_METHODS:
                if method != "POST":
                    response = client.request(method, CSP_REPORT_URI)
                    self.assertEqual(
                        response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                    )

            response = client.post(
                CSP_REPORT_URI,
                json=CSP_REPORT,
                headers={"Content-Type": CSP_REPORT_CONTENT_TYPE.decode()},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), True)
            row = await database.fetch_one(
                select([security_reports]).where(security_reports.c.id == 1)
            )
            assert row  # TODO: self.assert...
            self.assertEqual(row["report"], CSP_REPORT[CSP_REPORT_KEY])
            self.assertEqual(row["type"], ReportType.CSP)

    async def test_expect_ct(self) -> None:
        with TestClient(self.ruteni) as client:
            for method in ALL_METHODS:
                if method != "POST":
                    response = client.request(method, EXPECT_CT_URI)
                    self.assertEqual(
                        response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                    )

            response = client.post(
                EXPECT_CT_URI,
                json=EXPECT_CT_REPORT,
                headers={"Content-Type": EXPECT_CT_CONTENT_TYPE.decode()},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), True)
            row = await database.fetch_one(
                select([security_reports]).where(security_reports.c.id == 1)
            )
            assert row  # TODO: self.assert...
            self.assertEqual(row["report"], EXPECT_CT_REPORT[EXPECT_CT_KEY])
            self.assertEqual(row["type"], ReportType.EXPECT_CT)
