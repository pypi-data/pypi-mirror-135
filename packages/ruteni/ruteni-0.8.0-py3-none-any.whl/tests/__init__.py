import unittest


def build_test_suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    return loader.discover(start_dir="tests", top_level_dir=".")
