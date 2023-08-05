from collections.abc import Callable, Iterable
from typing import Optional, TypeVar

T = TypeVar("T")

Observer = Callable[[Optional[Iterable[T]], Optional[Iterable[T]]], None]


# https://github.com/dimsf/Python-observable-collections
class ObservableSet(set[T]):
    def __init__(self, elements: Optional[Iterable[T]] = None) -> None:
        super().__init__(elements or ())
        self.observers: set[Observer] = set()  # TODO: weakset

    def _notify(
        self, newElements: Optional[Iterable[T]], oldElements: Optional[Iterable[T]]
    ) -> None:
        for observer in self.observers:
            observer(newElements, oldElements)

    def subscribe(self, observer: Observer) -> None:
        self.observers.add(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self.observers.discard(observer)

    def add(self, element: T) -> None:
        super().add(element)
        self._notify((element,), None)

    def discard(self, element: T) -> None:
        super().discard(element)
        self._notify(None, (element,))

    remove = discard

    def clear(self) -> None:
        elements = tuple(self)
        super().clear()
        self._notify(None, elements)

    def pop(self) -> T:
        element = super().pop()
        self._notify(None, (element,))
        return element

    # TODO: __ior__, __iand__, __ixor__, __isub__
