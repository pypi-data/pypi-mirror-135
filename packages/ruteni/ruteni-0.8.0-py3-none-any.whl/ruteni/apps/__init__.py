from collections.abc import Iterable
from typing import Optional

from ruteni.routing.nodes import IterableNode
from ruteni.routing.types import Node
from ruteni.services import Service, ServiceSet


class AppNode(Service, IterableNode):
    def __init__(
        self,
        name: str,
        version: int,
        nodes: Iterable[Node],
        requires: Optional[ServiceSet] = None,
    ) -> None:
        Service.__init__(self, name, version, requires)
        IterableNode.__init__(self, nodes)


class LocalizedAppNode(AppNode):
    def __init__(
        self,
        name: str,
        version: int,
        nodes: Iterable[Node],
        languages: tuple[str, ...],
        requires: Optional[ServiceSet] = None,
    ) -> None:
        super().__init__(name, version, nodes, requires)
        self.languages = languages
