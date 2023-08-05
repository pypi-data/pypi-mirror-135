import unittest
from uuid import UUID

from ruteni.routing.extractors import int_extractor, uuid_extractor


class TestFunctionExtractors(unittest.TestCase):
    def test_int_extractor(self) -> None:
        # correct terminal int url path
        self.assertEqual(int_extractor("/42"), ("", 42))

        # correct non-terminal (`/`) int url path
        self.assertEqual(int_extractor("/42/"), ("/", 42))

        # correct non-terminal (`/foo`) int url path
        self.assertEqual(int_extractor("/42/foo"), ("/foo", 42))

        # empty string, slash and any random value
        self.assertIsNone(int_extractor(""))
        self.assertIsNone(int_extractor("/"))
        self.assertIsNone(int_extractor("/foo"))

        # missing leading slash
        self.assertIsNone(int_extractor("42"))

        # one incorrect-character
        self.assertIsNone(int_extractor("/42x"))
        self.assertIsNone(int_extractor("/x42"))

    def test_uuid_extractor(self) -> None:
        # correct terminal uuid url path
        self.assertEqual(
            uuid_extractor("/e595d345-61f7-4730-8e21-b7a6c7db33bb"),
            ("", UUID("e595d345-61f7-4730-8e21-b7a6c7db33bb")),
        )

        # correct non-terminal (`/`) uuid url path
        self.assertEqual(
            uuid_extractor("/e595d345-61f7-4730-8e21-b7a6c7db33bb/"),
            ("/", UUID("e595d345-61f7-4730-8e21-b7a6c7db33bb")),
        )

        # correct non-terminal (`/foo`) uuid url path
        self.assertEqual(
            uuid_extractor("/e595d345-61f7-4730-8e21-b7a6c7db33bb/foo"),
            ("/foo", UUID("e595d345-61f7-4730-8e21-b7a6c7db33bb")),
        )

        # empty string, slash and any random value
        self.assertIsNone(uuid_extractor(""))
        self.assertIsNone(uuid_extractor("/"))
        self.assertIsNone(uuid_extractor("/foo"))

        # missing leading slash
        self.assertIsNone(uuid_extractor("e595d345-61f7-4730-8e21-b7a6c7db33bb"))

        # one wrong character (`x` at the end)
        self.assertIsNone(uuid_extractor("/e595d345-61f7-4730-8e21-b7a6c7db33bx"))

        # one correct-character (`a` at the end) too long
        self.assertIsNone(uuid_extractor("/e595d345-61f7-4730-8e21-b7a6c7db33bba"))

        # one incorrect-character (`x` at the end) too long
        self.assertIsNone(uuid_extractor("/e595d345-61f7-4730-8e21-b7a6c7db33bbx"))


class TestPrefixExtractor(unittest.TestCase):
    def test_call(self) -> None:
        pass
