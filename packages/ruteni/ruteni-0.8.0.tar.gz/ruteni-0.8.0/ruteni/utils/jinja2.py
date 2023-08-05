from pathlib import Path

from anyio import open_file

import jinja2


async def get_template_from_path(path: Path) -> jinja2.Template:
    async with await open_file(path) as f:
        content = await f.read()
    return jinja2.Template(content, enable_async=True)


def get_template_env(directory: Path) -> jinja2.Environment:
    loader = jinja2.FileSystemLoader(directory)
    return jinja2.Environment(loader=loader, autoescape=True, enable_async=True)
