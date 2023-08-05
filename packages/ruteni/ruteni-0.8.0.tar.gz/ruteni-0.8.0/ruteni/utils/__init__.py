from importlib import import_module
from typing import Any


def load_symbol(dotpath: str) -> Any:
    """load symbol in module.  symbol is right-most segment"""
    module_, symbol = dotpath.rsplit(".", maxsplit=1)
    m = import_module(module_)
    return getattr(m, symbol)
