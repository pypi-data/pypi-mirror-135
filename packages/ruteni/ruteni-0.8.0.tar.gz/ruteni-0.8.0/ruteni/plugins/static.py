import logging

from ruteni.config import config
from ruteni.routing.nodes.http.static import StaticHTTPNode

logger = logging.getLogger(__name__)

directories = config.get("RUTENI_DEVEL_STATIC_DIRECTORIES")

node = StaticHTTPNode(directories.split(":"))

if not config.is_devel:
    logger.warn("static nodes should only be used in development")
