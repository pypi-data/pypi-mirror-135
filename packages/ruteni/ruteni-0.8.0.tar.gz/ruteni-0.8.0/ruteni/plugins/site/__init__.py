from pkg_resources import resource_filename
from ruteni.config import config
from ruteni.content import TEXT_PLAIN_CONTENT_TYPE, Content
from ruteni.routing import current_path_is
from ruteni.routing.nodes.http.content import HTTPContentNode
from ruteni.routing.nodes.http.file import FileNode

ABUSE_URL: str = config.get("RUTENI_SITE_ABUSE_URL")
SITE_NAME: str = config.get("RUTENI_SITE_NAME")
SITE_DOMAIN: str = config.get("RUTENI_SITE_DOMAIN")
LOGO_PATH: str = config.get(
    "RUTENI_SITE_LOGO_PATH", default=resource_filename(__name__, "/resources/logo.svg")
)
FAVICON_PATH: str = config.get(
    "RUTENI_SITE_FAVICON_PATH",
    default=resource_filename(__name__, "/resources/favicon.ico"),
)
FAVICON_LOCATION: str = config.get(
    "RUTENI_SITE_FAVICON_LOCATION", default="/favicon.ico"
)
ROBOT_TEXT: bytes = config.get(
    "RUTENI_SITE_ROBOT_TEXT", cast=str.encode, default="User-agent: *\nDisallow:"
)


IMAGE_ICON_CONTENT_TYPE = "image/x-icon"


# TODO: use an Icon from ruteni.utils.icon

# FAVICON_DATA = b64decode(
#     "AAABAAEAEBACAAEAAQBWAAAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/"
#     "YQAAAB1JREFUOI1j/P///38GCgATJZpHDRg1YNSAwWQAAGvKBByn4XVTAAAAAElFTkSuQmCC"
# )
# node = HTTPContentNode(
#     current_path_is("/favicon.ico"), Content(FAVICON_DATA, IMAGE_ICON_CONTENT_TYPE)
# )

favicon_node = FileNode(
    current_path_is(FAVICON_LOCATION), FAVICON_PATH, media_type=IMAGE_ICON_CONTENT_TYPE
)

robots_node = HTTPContentNode(
    current_path_is("/robots.txt"), Content(ROBOT_TEXT, TEXT_PLAIN_CONTENT_TYPE)
)
