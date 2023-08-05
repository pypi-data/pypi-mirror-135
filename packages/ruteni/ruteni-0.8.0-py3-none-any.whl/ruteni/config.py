import logging
import os
from typing import Any

from starlette.config import Config as StarletteConfig

logger = logging.getLogger(__name__)


class Config(StarletteConfig):
    def __init__(self) -> None:
        super().__init__(os.environ.get("RUTENI_CONFIG", ".env"))

    def set(self, key: str, value: Any) -> None:
        self.environ[key] = value

    @property
    def env(self) -> str:
        return self.get("RUTENI_ENV", default="production")

    @property
    def is_devel(self) -> bool:
        return self.env == "development"

    @property
    def is_debug(self) -> bool:
        return self.get("RUTENI_DEBUG", cast=bool, default=False)


config = Config()
