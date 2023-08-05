from collections.abc import Iterable, Iterator
from typing import Optional

from ruteni.core.types import App
from ruteni.observable import ObservableSet
from ruteni.routing.nodes import TScope
from ruteni.routing.types import Node, Route


class NodeStat:
    def __init__(self) -> None:
        self.hits = 0
        self.misses = 0


class TupleStatsNode:
    def __init__(self, node_set: ObservableSet[Node]) -> None:
        # TODO: any sorted container we could use?
        # http://www.grantjenks.com/docs/sortedcontainers/
        # https://boltons.readthedocs.io/en/latest/setutils.html
        # https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set
        children = [(node, NodeStat()) for node in node_set]

        def on_change(
            newNodes: Optional[Iterable[Node]], oldNodes: Optional[Iterable[Node]]
        ) -> None:
            if newNodes is not None:
                for node in newNodes:
                    children.append((node, NodeStat()))
            if oldNodes is not None:
                for node in oldNodes:  # TODO: single scan
                    for child in children:
                        if child[0] == node:
                            children.remove(child)
                            break

        node_set.subscribe(on_change)
        self.children = children

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        for node, stat in self.children:
            response = await node(scope, route)
            if response is not None:
                stat.hits += 1
                return response
            else:
                stat.misses += 1
        return None

    def __iter__(self) -> Iterator[Node]:
        return (child[0] for child in self.children)

    def sort(self) -> None:
        # TODO: make sure the change is atomic
        self.children.sort(key=lambda child: child[1].hits, reverse=True)


class DictStatsNode:
    def __init__(self, node_set: ObservableSet[Node]) -> None:
        self.children = {node: NodeStat() for node in node_set}
        node_set.subscribe(self._on_change)  # TODO: unsubscribe/weakref

    def __repr__(self) -> str:
        return "%s()" % self.__class__.__name__

    async def __call__(self, scope: TScope, route: Route) -> Optional[App]:
        for node, stat in self.children.items():
            response = await node(scope, route)
            if response is not None:
                stat.hits += 1
                return response
            else:
                stat.misses += 1
        return None

    def _on_change(
        self, newNodes: Optional[Iterable[Node]], oldNodes: Optional[Iterable[Node]]
    ) -> None:
        if newNodes is not None:
            for node in newNodes:
                self.children[node] = NodeStat()
        if oldNodes is not None:
            for node in oldNodes:
                del self.children[node]

    def __iter__(self) -> Iterator[Node]:
        return iter(self.children.keys())

    def sort(self) -> None:
        # since python 3.7, the order of dict entries is guaranteed
        # TODO: make sure the change is atomic
        self.children = dict(
            sorted(self.children.items(), key=lambda t: t[1].hits, reverse=True)
        )
