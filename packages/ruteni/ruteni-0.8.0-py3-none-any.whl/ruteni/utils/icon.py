from typing import Optional

import PIL.IcoImagePlugin
import PIL.PngImagePlugin
from ruteni.types import PathLike
from starlette.datastructures import URLPath

PURPOSE_VALUE_SET = set(("any", "monochrome", "maskable"))


class Icon:
    def __init__(self, name: str, filename: PathLike, purpose: Optional[str] = None):
        self.name = name
        self.filename = filename
        if purpose and not set(purpose.split()).issubset(PURPOSE_VALUE_SET):
            raise ValueError("invalid purpose value")
        self.purpose = purpose  # TODO: store set?

    @property
    def src(self) -> URLPath:
        return str(self.name)

    @property
    def sizes(self) -> str:
        raise NotImplementedError

    @property
    def type(self) -> str:
        raise NotImplementedError

    @property
    def image(self) -> PIL.ImageFile.ImageFile:
        raise NotImplementedError

    def has(self, size: str) -> bool:
        return size in self.sizes.split()

    def to_dict(self) -> dict:
        result = dict(src=self.src, sizes=self.sizes, type=self.type)
        if self.purpose:
            result["purpose"] = self.purpose
        return result


class PngIcon(Icon):
    @property
    def sizes(self) -> str:
        return "{}x{}".format(*self.image.size)

    @property
    def type(self) -> str:
        return "image/png"

    @property
    def image(self) -> PIL.ImageFile.ImageFile:
        with open(self.filename, "rb") as fp:
            return PIL.PngImagePlugin.PngImageFile(fp=fp, filename=self.filename)


class IcoIcon(Icon):
    @property
    def sizes(self) -> str:
        return " ".join(
            f"{width}x{height}" for width, height in sorted(self.image.info["sizes"])
        )

    @property
    def type(self) -> str:
        return "image/x-icon"

    @property
    def image(self) -> PIL.ImageFile.ImageFile:
        with open(self.filename, "rb") as fp:
            return PIL.IcoImagePlugin.IcoImageFile(fp=fp, filename=self.filename)
