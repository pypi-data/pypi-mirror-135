import argparse
import logging
import os
import tempfile
from pathlib import Path

import asyncssh
import uvicorn
from asgiref.typing import HTTPScope, WebSocketScope

from ruteni.apis import api_nodes
from ruteni.app import Ruteni
from ruteni.config import config
from ruteni.routing import current_path_is
from ruteni.routing.extractors import PrefixExtractor
from ruteni.routing.nodes import ExtractorNode, IterableNode
from ruteni.routing.nodes.http import load_http_node_entry_point
from ruteni.routing.nodes.stats import TupleStatsNode
from ruteni.routing.nodes.websocket import WebSocketEntryPointNode
from ruteni.routing.types import HTTPNode, WebSocketNode
from ruteni.utils.jwkset import KeyCollection

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--test-dir",
    type=lambda p: Path(p).absolute(),
    default=Path(tempfile.mkdtemp()).absolute(),
    help="Path to the test directory",
)
parser.add_argument(
    "-s", "--static-dir", required=False, help="Path to the static directory"
)
args = parser.parse_args()

PRIVATE_KEYS = str(args.test_dir / "private_keys.json")
PUBLIC_KEYS = str(args.test_dir / "public_keys.json")
DB_URL = "sqlite:///" + str(args.test_dir / "test.db")

key_collection = KeyCollection(args.test_dir, True)
key_collection.generate()
key_collection.export(PUBLIC_KEYS, PRIVATE_KEYS)

SERVER_HOST_KEYS = str(args.test_dir / "ssh_host_key")

if not os.path.exists(SERVER_HOST_KEYS):
    key = asyncssh.generate_private_key("ssh-rsa")
    key.write_private_key(SERVER_HOST_KEYS)
    key.write_public_key(SERVER_HOST_KEYS + ".pub")

static_dir = str(args.static_dir or Path(__file__).parent / "dist" / "static")

config.set("RUTENI_ENV", "development")
config.set("RUTENI_DEVEL_STATIC_DIRECTORIES", static_dir)
config.set("RUTENI_SITE_NAME", "Ruteni test")
config.set("RUTENI_SITE_DOMAIN", "accot.fr")
config.set("RUTENI_DATABASE_URL", DB_URL)
config.set("RUTENI_SESSION_SECRET_KEY", "secret-key")
config.set("RUTENI_JWKEYS_FILE", PRIVATE_KEYS)
config.set("RUTENI_SITE_ABUSE_URL", "<abuse_url>")
config.set("RUTENI_VERIFICATION_FROM_ADDRESS", "Accot <contact@accot.fr>")
config.set("RUTENI_SSHD_SERVER_HOST_KEYS", SERVER_HOST_KEYS)

services = {
    "ruteni:auth-api",
    "ruteni:database",
    "ruteni:health-check",
    "ruteni:logging-api",
    "ruteni:nng",
    "ruteni:presence",
    "ruteni:scheduler",
    "ruteni:security-api",
    "ruteni:smtpd",
    "ruteni:sshd",
    "ruteni:store-api",
    "ruteni:user-api",
}


http_nodes: list[HTTPNode] = [
    ExtractorNode(PrefixExtractor("/api"), TupleStatsNode(api_nodes)),
    ExtractorNode(
        PrefixExtractor("/app"),
        IterableNode(
            [
                ExtractorNode(
                    PrefixExtractor("/store"),
                    load_http_node_entry_point("ruteni", "store-app"),
                )
            ]
        ),
    ),
    ExtractorNode(
        PrefixExtractor("/ap"),
        IterableNode(
            [
                ExtractorNode(
                    PrefixExtractor("/register"),
                    load_http_node_entry_point("ruteni", "register"),
                )
            ]
        ),
    ),
    load_http_node_entry_point("ruteni", "robots"),
    load_http_node_entry_point("ruteni", "favicon"),
]

if config.is_devel:
    http_nodes.append(
        ExtractorNode(
            PrefixExtractor("/static"), load_http_node_entry_point("ruteni", "static")
        )
    )


websocket_nodes: list[WebSocketNode] = [
    WebSocketEntryPointNode(current_path_is("/socket.io/"), "ruteni", "socketio")
]


# def getCaseCount(
#     scope: WebSocketScope, route: Route
# ) -> Optional[WebSocketApp]:
#     return WebSocket() if scope["path"] == "/getCaseCount" else None
# websocket_nodes.append(getCaseCount)

print({"http": len(http_nodes), "websocket": len(websocket_nodes)})

app = Ruteni(
    http_node=IterableNode[HTTPScope](http_nodes),
    websocket_node=IterableNode[WebSocketScope](websocket_nodes),
    services=services,
)

uvicorn.run(app, host="127.0.0.1", port=8000, lifespan="on")
