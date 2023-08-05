import os
import unittest
from unittest.mock import patch

from starlette.testclient import TestClient

from .config import USER_EMAIL, USER_LOCALE, USER_NAME, clear_database, test_env

with patch.dict(os.environ, test_env):
    from ruteni.apis.users import UnknownUserException, add_user
    from ruteni.app import Ruteni
    from ruteni.plugins.groups import (
        GroupStatus,
        InvalidExpressionException,
        UnknownGroupException,
        add_group,
        add_user_to_group,
        test_group_condition,
    )


class GroupsTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.ruteni = Ruteni(services={"ruteni:user-api"})

    def tearDown(self) -> None:
        clear_database()

    async def test_add_user_to_group(self) -> None:
        with TestClient(self.ruteni):
            user_info = await add_user(USER_NAME, USER_EMAIL, USER_LOCALE)
            user_id = user_info.id
            with self.assertRaises(UnknownGroupException):
                await add_user_to_group(user_id, "foo")
            await add_group("foo")
            self.assertEqual(await add_user_to_group(user_id, "foo"), 1)

    async def test_test_group_condition(self) -> None:
        with TestClient(self.ruteni):

            with self.assertRaises(UnknownUserException):
                await test_group_condition(2, "foo")

            user_info = await add_user(USER_NAME, USER_EMAIL, USER_LOCALE)
            user_id = user_info.id

            self.assertFalse(await test_group_condition(user_id, "FALSE"))
            self.assertTrue(await test_group_condition(user_id, "TRUE"))

            with self.assertRaises(InvalidExpressionException):
                await test_group_condition(user_id, "(")

            self.assertFalse(await test_group_condition(user_id, "qux"))
            self.assertTrue(await test_group_condition(user_id, "not qux"))

            await add_group("foo")
            await add_group("bar")
            await add_group("baz")

            await add_user_to_group(user_id, "foo")
            self.assertTrue(await test_group_condition(user_id, "foo"))
            self.assertTrue(await test_group_condition(user_id, "foo:member"))
            self.assertFalse(await test_group_condition(user_id, "not foo:member"))
            self.assertFalse(await test_group_condition(user_id, "foo:manager"))
            self.assertTrue(await test_group_condition(user_id, "not foo:manager"))
            self.assertFalse(await test_group_condition(user_id, "foo:owner"))
            self.assertTrue(await test_group_condition(user_id, "not foo:owner"))
            self.assertFalse(await test_group_condition(user_id, "foo and bar"))
            self.assertTrue(await test_group_condition(user_id, "foo or bar"))
            self.assertTrue(await test_group_condition(user_id, "foo and not bar"))
            self.assertFalse(await test_group_condition(user_id, "foo and qux"))
            self.assertTrue(await test_group_condition(user_id, "foo or qux"))
            self.assertTrue(await test_group_condition(user_id, "foo and not qux"))
            self.assertFalse(await test_group_condition(user_id, "foo and bar and baz"))
            self.assertFalse(await test_group_condition(user_id, "foo and bar and qux"))

            await add_user_to_group(user_id, "bar", GroupStatus.manager)
            self.assertTrue(await test_group_condition(user_id, "foo"))
            self.assertTrue(await test_group_condition(user_id, "foo and bar"))
            self.assertTrue(await test_group_condition(user_id, "foo and bar:manager"))
            self.assertFalse(await test_group_condition(user_id, "foo and bar:owner"))
            self.assertFalse(await test_group_condition(user_id, "foo and bar and baz"))
            self.assertTrue(
                await test_group_condition(user_id, "foo and bar and not baz")
            )
            self.assertTrue(
                await test_group_condition(user_id, "foo and (qux or not baz)")
            )

            await add_user_to_group(user_id, "baz", GroupStatus.owner)
            self.assertTrue(await test_group_condition(user_id, "foo"))
            self.assertTrue(await test_group_condition(user_id, "foo and bar"))
            self.assertTrue(await test_group_condition(user_id, "foo and bar and baz"))
            self.assertTrue(await test_group_condition(user_id, "baz:manager"))
            self.assertTrue(await test_group_condition(user_id, "baz:owner"))


if __name__ == "__main__":
    unittest.main()
