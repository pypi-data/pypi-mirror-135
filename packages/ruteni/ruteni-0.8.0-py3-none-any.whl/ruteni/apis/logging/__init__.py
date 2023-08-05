import enum
import logging

import pyrfc3339
from asgiref.typing import HTTPScope
from ruteni.apis import APINode
from ruteni.apis.users import users
from ruteni.core.types import HTTPApp, HTTPReceive
from ruteni.endpoints import POST
from ruteni.exceptions import HTTPException
from ruteni.plugins.sqlalchemy import metadata
from ruteni.responses import Response
from ruteni.routing import current_path_is
from ruteni.routing.nodes.http import HTTPAppMapNode
from ruteni.services.database import database
from ruteni.utils.form import get_json_body
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Table

logger = logging.getLogger(__name__)

# https://github.com/fluent/fluent-logger-python
# @todo https://nuculabs.dev/2021/05/18/fastapi-uvicorn-logging-in-production/
# logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class Level(enum.Enum):
    trace = 1
    debug = 2
    info = 3
    warn = 4
    error = 5


logs = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    Column("level", Enum(Level), nullable=False),
    Column("logger", String(255), nullable=False),
    Column("message", String, nullable=False),
    Column("timestamp", DateTime, nullable=False),
    Column("stacktrace", String),
)


async def log_app(scope: HTTPScope, receive: HTTPReceive) -> HTTPApp:
    """
    {
        "logs": [
            {
                "message": "name-update2",
                "level": <Level.warn: 4>,
                "logger": "registration-homepage",
                "timestamp": datetime.datetime(
                    2021, 10, 1, 21, 27, 55, 700000, tzinfo=datetime.timezone.utc
                ),
                "stacktrace": "    at HTMLInputElement.name-update (http://127.0.0.1:8000/static/components/registration-homepage/index.js:25:28)",
                "user_id": None,
            }
        ]
    }
    """
    try:
        pkt = await get_json_body(scope, receive)
    except HTTPException as exc:
        return exc.response

    report = pkt["logs"]

    for log in report:
        log["level"] = Level[log["level"]]
        log["timestamp"] = pyrfc3339.parse(log["timestamp"])
        if log["stacktrace"] == "":
            log["stacktrace"] = None
        # TODO:  request.user.id if request.user.is_authenticated else None
        log["user_id"] = None

    await database.execute_many(logs.insert(), report)
    return Response()


api_node = APINode(
    "logging", 1, [HTTPAppMapNode(current_path_is("/log"), POST(log_app))]
)
