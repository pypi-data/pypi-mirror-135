import logging
from pathlib import Path

import html5lib
from html5lib.treewalkers import getTreeWalker

logger = logging.getLogger(__name__)

dependencies: dict[str, set[str]] = {}


def load_component_dir(directory: Path) -> None:
    for node in directory.iterdir():
        if node.is_file():
            if node.suffix == ".js":
                pass  # context.add_file_route(node.name + ".js", node)
            else:
                logger.warn(f"file {node} ignored")
        else:
            index_js = node.joinpath("index.js")
            if index_js.exists():
                pass  # context.add_file_route(node.name + ".js", index_js)

                index_html = node.joinpath("index.html")
                if index_html.exists():
                    with open(index_html, "rb") as f:
                        fragment = html5lib.parseFragment(f)
                    walker = getTreeWalker("etree")
                    stream = walker(fragment)
                    dependencies[node.name] = set()
                    for element in stream:
                        if element["type"] == "StartTag":
                            if "-" in element["name"]:
                                dependencies[node.name].add(element["name"])
                    pass  # context.add_file_route(node.name + ".html", index_html)

                index_css = node.joinpath("index.css")
                if index_css.exists():
                    pass  # context.add_file_route(node.name + ".css", index_css)
            else:
                logger.warn(f"missing index.js in '{node}'")
