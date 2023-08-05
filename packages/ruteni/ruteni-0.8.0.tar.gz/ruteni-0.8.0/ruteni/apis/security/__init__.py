import enum
import logging
from collections.abc import Mapping, Sequence
from typing import Optional

from asgiref.typing import HTTPScope
from ruteni.apis import APINode
from ruteni.apis.users import users
from ruteni.config import config
from ruteni.core.types import HTTPApp, HTTPReceive
from ruteni.endpoints import POST
from ruteni.exceptions import HTTPException
from ruteni.plugins.sqlalchemy import metadata
from ruteni.routing import current_path_is
from ruteni.routing.nodes.http import HTTPAppMapNode
from ruteni.services.database import database
from ruteni.utils.form import get_json_body
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Table, func
from sqlalchemy_utils.types.json import JSONType
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


# TODO: add middleware that checks that csp header is set on html?
# https://web.dev/csp-xss/
# https://flask.palletsprojects.com/en/2.0.x/security/
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
# https://github.com/shieldfy/APINode-Security-Checklist/blob/master/README.md
# https://mechlab-engineering.de/2019/01/security-testing-and-deployment-of-an-api-release-your-flask-app-to-the-internet/
# https://pypi.org/project/asgi-sage/
# https://scotthelme.co.uk/a-new-security-header-expect-ct/
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
# https://hstspreload.org/

EXPECT_CT_MAX_AGE: int = config.get(
    "RUTENI_SECURITY_EXPECT_CT_MAX_AGE", cast=int, default=60  # 86400  # 1 day
)
HSTS_MAX_AGE: int = config.get(
    "RUTENI_SECURITY_HSTS_MAX_AGE", cast=int, default=63072000  # 2 years
)

CSP_REPORT_CONTENT_TYPE = b"application/csp-report"
EXPECT_CT_CONTENT_TYPE = b"application/expect-ct-report+json"
CSP_REPORT_KEY = "csp-report"
EXPECT_CT_KEY = "expect-ct-report"


class ReportType(enum.Enum):
    CSP = 1
    EXPECT_CT = 2


security_reports = Table(
    "security_reports",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", Enum(ReportType), nullable=False),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=True),
    Column("report", JSONType, nullable=False),
    Column("timestamp", DateTime, nullable=False, server_default=func.now()),
)


async def csp_report(scope: HTTPScope, receive: HTTPReceive) -> HTTPApp:
    """
    {
        "csp-report": {
            "document-uri": "http://localhost:8000/app/store/",
            "referrer": "",
            "violated-directive": "script-src-elem",
            "effective-directive": "script-src-elem",
            "original-policy": "default-src 'self'; worker-src 'self'; frame-src 'none'; child-src 'none'; object-src 'none'; require-trusted-types-for 'script'; report-uri /api/security/v1/csp-report/;",
            "disposition": "enforce",
            "blocked-uri": "inline",
            "line-number": 16,
            "source-file": "http://localhost:8000/app/store/",
            "status-code": 200,
            "script-sample": "",
        }
    }
    """
    try:
        pkt = await get_json_body(scope, receive, CSP_REPORT_CONTENT_TYPE)
    except HTTPException as exc:
        return exc.response
    report = pkt[CSP_REPORT_KEY]
    # user_id = request.user.id if request.user.is_authenticated else None
    await database.execute(
        security_reports.insert().values(type=ReportType.CSP, report=report)  # user_id=
    )
    return JSONResponse(True)


async def expect_ct(scope: HTTPScope, receive: HTTPReceive) -> HTTPApp:
    """
    https://shaunc.com/blog/article/implementing-a-reporturi-endpoint-for-expectct-and-other-headers~Xdf4cU8EurV1
    https://www.tpeczek.com/2017/05/preparing-for-chromes-certificate.html
    {
        "expect-ct-report": {
            "date-time": "2017-05-05T12:45:00Z",
            "hostname": "example.com",
            "port": 443,
            "effective-expiration-date": "2017-05-05T12:45:00Z",
            ...
        }
    }
    """
    try:
        pkt = await get_json_body(scope, receive, EXPECT_CT_CONTENT_TYPE)
    except HTTPException as exc:
        return exc.response

    report = pkt[EXPECT_CT_KEY]

    # user_id = request.user.id if request.user.is_authenticated else None
    await database.execute(
        security_reports.insert().values(type=ReportType.EXPECT_CT, report=report)
    )
    return JSONResponse(True)


api_node = APINode(
    "security",
    1,
    [
        HTTPAppMapNode(current_path_is("/csp-report"), POST(csp_report)),
        HTTPAppMapNode(current_path_is("/expect-ct"), POST(expect_ct)),
    ],
    {database},
)

CSP_REPORT_URI = ""  # csp_report_endpoint.url_path
EXPECT_CT_URI = ""  # expect_ct_endpoint.url_path


def get_security_headers(
    connect: bool = False,
    img: bool = False,
    manifest: bool = False,
    script: bool = False,
    style: bool = False,
    worker: bool = False,
    csp_report_only: bool = False,
    trusted_types: Optional[Sequence[str]] = ("default", "dompurify"),
) -> Mapping[str, str]:
    # https://csp.withgoogle.com/docs/strict-csp.html
    csp = f"report-uri {CSP_REPORT_URI}; base-uri 'none'; default-src 'none'"
    if connect:
        csp += "; connect-src 'self'"
    if img:
        csp += "; img-src 'self'"
    if manifest:
        csp += "; manifest-src 'self'"
    if script:
        csp += "; script-src 'self'"
    if style:
        csp += "; style-src 'self'"
    if worker:
        csp += "; worker-src 'self'"
    if trusted_types:
        csp += "; require-trusted-types-for 'script'"
        csp += "; trusted-types " + " ".join(trusted_types)
    return {
        "Content-Security-Policy" + ("-Report-Only" if csp_report_only else ""): csp,
        "Strict-Transport-Security": f"max-age={HSTS_MAX_AGE}; includeSubDomains; preload",
        "Expect-CT": f'max-age={EXPECT_CT_MAX_AGE}, enforce, report-uri="{EXPECT_CT_URI}"',
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "deny",
        "X-XSS-Protection": "1; mode=block",
        "Access-Control-Allow-Methods": "GET",
    }
