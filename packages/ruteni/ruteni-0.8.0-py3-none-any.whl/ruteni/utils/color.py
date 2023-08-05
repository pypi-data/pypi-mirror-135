from __future__ import annotations

from webcolors import CSS3_NAMES_TO_HEX, HEX_COLOR_RE


class Color(str):
    def __new__(cls, p_string: str) -> Color:
        if p_string not in CSS3_NAMES_TO_HEX and not HEX_COLOR_RE.match(p_string):
            raise ValueError(f"invalid color {p_string}")
        return str.__new__(cls, p_string)
