import unittest

from ruteni.utils.color import Color
from webcolors import CSS3_NAMES_TO_HEX


class ColorTestCase(unittest.TestCase):
    def test_color(self) -> None:
        with self.assertRaises(ValueError):
            Color("#f")
        with self.assertRaises(ValueError):
            Color("foo")
        for name, hex_value in CSS3_NAMES_TO_HEX.items():
            self.assertEqual(Color(name), name)
            self.assertEqual(Color(hex_value), hex_value)
