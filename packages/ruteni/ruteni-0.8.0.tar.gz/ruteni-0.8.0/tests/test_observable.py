import unittest
from collections.abc import Iterable
from typing import Optional

from ruteni.observable import ObservableSet


class TestObservableSet(unittest.TestCase):
    def test_add(self) -> None:
        def observer(
            newInts: Optional[Iterable[int]], oldInts: Optional[Iterable[int]]
        ) -> None:
            self.assertIsNotNone(newInts)
            assert newInts is not None  # for the type checker
            self.assertEqual(set(newInts), {1})
            self.assertIsNone(oldInts)

        node_set = ObservableSet[int]()
        node_set.subscribe(observer)
        node_set.add(1)

    def test_discard(self) -> None:
        def observer(
            newInts: Optional[Iterable[int]], oldInts: Optional[Iterable[int]]
        ) -> None:
            self.assertIsNone(newInts)
            self.assertIsNotNone(oldInts)
            assert oldInts is not None  # for the type checker
            self.assertEqual(set(oldInts), {1})

        node_set = ObservableSet[int]({1})
        node_set.subscribe(observer)
        node_set.discard(1)

    def test_clear(self) -> None:
        def observer(
            newInts: Optional[Iterable[int]], oldInts: Optional[Iterable[int]]
        ) -> None:
            self.assertIsNone(newInts)
            self.assertIsNotNone(oldInts)
            assert oldInts is not None  # for the type checker
            self.assertEqual(set(oldInts), {1, 2})

        node_set = ObservableSet[int]({1, 2})
        node_set.subscribe(observer)
        node_set.clear()
