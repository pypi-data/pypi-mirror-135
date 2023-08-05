import logging
from typing import Optional

import ruteni.apis.auth
import ruteni.plugins.quotquot
from asgiref.typing import HTTPScope
from pkg_resources import resource_filename
from ruteni.apis import APINode
from ruteni.apis.security import get_security_headers
from ruteni.apps import LocalizedAppNode
from ruteni.core.types import HTTPApp
from ruteni.endpoints import GET
from ruteni.routing import current_path_is
from ruteni.routing.nodes import SlashRedirectNode
from ruteni.routing.nodes.http import HTTPAppMapNode
from ruteni.routing.nodes.http.file import CustomFileNode, FileNode
from ruteni.routing.types import FileMatch, PathLike, Route
from starlette.datastructures import URLPath
from starlette.responses import JSONResponse
from werkzeug.datastructures import LanguageAccept
from werkzeug.http import parse_accept_header

logger = logging.getLogger(__name__)

# https://medium.com/@applification/progressive-web-app-splash-screens-80340b45d210

MANIFEST_NAME = "store.webmanifest"


def language_match(url_path: URLPath, file_path_pattern: str) -> FileMatch:
    url_match = current_path_is(url_path)

    def match(scope: HTTPScope, route: Route) -> Optional[PathLike]:
        if not url_match(route):
            return None
        for key, val in scope["headers"]:
            if key == b"accept-language":
                language_accept = parse_accept_header(val.decode(), LanguageAccept)
                language = language_accept.best_match(app_node.languages)
                break
        else:
            language = None
        return file_path_pattern.format(language or "en-US")

    return match


nodes = (
    FileNode(
        current_path_is("/"),
        resource_filename(__name__, "resources/index.html"),
        headers=get_security_headers(
            connect=True, img=True, script=True, manifest=True
        ),
        media_type="text/html",
    ),
    CustomFileNode(
        language_match("/sw.js", resource_filename(__name__, "resources/{}/sw.js")),
        media_type="application/javascript",
    ),
    CustomFileNode(
        language_match(
            "/manifest.json", resource_filename(__name__, "resources/{}/manifest.json")
        ),
        media_type="application/manifest+json",
    ),
    CustomFileNode(
        language_match(
            "/resources.json",
            resource_filename(__name__, "resources/{}/resources.json"),
        ),
        media_type="application/json",
    ),
    FileNode(
        current_path_is("/favicon.ico"),
        resource_filename(__name__, "resources/favicon.ico"),
        media_type="image/x-icon",
    ),
    # FileNode(
    #     current_path_is("/routes.json"),
    #     resource_filename(__name__, "resources/routes.json"),
    #     media_type="application/json",
    # ),
    SlashRedirectNode(),
)

app_node = LocalizedAppNode("store", 1, nodes, ("fr-FR", "en-US"))

"""
store_pwa = PWANode(
    "/store/*",
    1,
    resource_filename(__name__, "resources/"),
    theme_color=Color("#2196f3"),
    background_color=Color("#2196f3"),
    display=Display.STANDALONE,
)
"""

"""
for size in (192, 512):
    icon = PngIcon(
        name=f"icon-{size}x{size}",
        filename=f"images/icons/icon-{size}x{size}.png",  # "FIXME" config.static_dir / f"@ruteni/store/v1/images/icons/icon-{size}x{size}.png" / path,
        purpose="any maskable",
    )
    store_pwa.add_icon(icon)

store_pwa.add_i18n(
    Locale("en", "US"),
    full_name="Ruteni app store",
    short_name="app store",
    description="A simple app store",
    categories=["app", "store"],
)

store_pwa.add_i18n(
    Locale("fr", "FR"),
    full_name="Magasin d'applications de Ruteni",
    short_name="Magasin d'applications",
    description="Un magasin d'applications simple",
    categories=["applications", "magasin"],
)
"""


async def list_apps(scope: HTTPScope) -> HTTPApp:
    result: list = []
    """
    for app in AppNode.all_apps:
        # ignore the app store itself
        if app is store:
            continue

        # if the app requires special access rights, check that the user statifies them
        if isinstance(app, UserAccessMixin) and not (
            request.user.is_authenticated and app.accessible_to(request.user.id)
        ):
            continue

        if isinstance(app, PWANode):
            locale = get_locale_from_request(request, app.available_locales)
            app_info = app.get_manifest(locale)
        else:
            app_info = dict(name=app.name)

        result.append(app_info)
    """
    return JSONResponse(result)


api_node = APINode(
    "store", 1, [HTTPAppMapNode(current_path_is("/list"), GET(list_apps))]
)
