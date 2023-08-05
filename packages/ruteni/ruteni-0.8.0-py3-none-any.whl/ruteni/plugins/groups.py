import enum
import logging
from collections.abc import Sequence
from typing import NamedTuple

from boolean import BooleanAlgebra, boolean
from ruteni.apis.users import assert_user_exists, users
from ruteni.plugins.sqlalchemy import metadata
from ruteni.services.database import database

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    and_,
    event,
    func,
    text,
)
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql import select

logger = logging.getLogger(__name__)


class UnknownGroupException(Exception):
    def __init__(self, group_name: str) -> None:
        super().__init__(f"unknown group: {group_name}")
        self.group_name = group_name


class InvalidExpressionException(Exception):
    def __init__(self, expression: str) -> None:
        super().__init__(f"unknown expression: {expression}")
        self.expression = expression


class GroupStatus(enum.Enum):
    member = 1
    manager = 2
    owner = 3


groups = Table(
    "groups",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(28), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    Column("disabled_at", DateTime, default=None),
)

Index(
    "ix_groups_name_not_disabled",
    groups.c.name,
    unique=True,
    sqlite_where=groups.c.disabled_at.is_(None),
    postgresql_where=groups.c.disabled_at.is_(None),
)

memberships = Table(
    "memberships",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id), nullable=False),
    Column("group_id", Integer, ForeignKey(groups.c.id), nullable=False),
    Column("status", Enum(GroupStatus), nullable=False),
    # Column("added_by", Integer, ForeignKey(users.c.id), nullable=False),
    Column("added_at", DateTime, nullable=False, server_default=func.now()),
    # Column("disabled_by", Integer, ForeignKey(users.c.id), default=None),
    Column("disabled_at", DateTime, default=None),
)

Index(
    "ix_memberships_user_group_not_disabled",
    memberships.c.user_id,
    memberships.c.group_id,
    unique=True,
    sqlite_where=memberships.c.disabled_at.is_(None),
    postgresql_where=memberships.c.disabled_at.is_(None),
)


def after_create(target: Table, connection: Connection, **kwargs):  # type: ignore
    connection.execute(text("INSERT INTO %s (name) VALUES ('admin')" % target.name))


event.listen(groups, "after_create", after_create)


class MembershipInfo(NamedTuple):
    group: str
    status: GroupStatus


async def get_user_groups(user_id: int) -> Sequence[str]:
    await assert_user_exists(user_id)
    return tuple(
        membership_info.group for membership_info in await get_user_memberships(user_id)
    )


async def get_user_memberships(user_id: int) -> Sequence[MembershipInfo]:
    await assert_user_exists(user_id)
    return tuple(
        MembershipInfo(row["name"], row["status"])
        for row in await database.fetch_all(
            select([groups.c.name, memberships.c.status])
            .select_from(memberships.join(groups).join(users))
            .where(
                and_(
                    memberships.c.user_id == user_id,
                    users.c.disabled_at.is_(None),
                    groups.c.disabled_at.is_(None),
                    memberships.c.disabled_at.is_(None),
                )
            )
        )
    )


async def add_group(name: str) -> int:
    return await database.execute(groups.insert().values(name=name))


async def add_user_to_group(
    user_id: int, group_name: str, status: GroupStatus = GroupStatus.member
) -> int:
    await assert_user_exists(user_id)

    # TODO: try to use insert(memberships).from_select(...)
    group_id = await database.fetch_val(
        select([groups.c.id]).where(
            and_(groups.c.name == group_name, groups.c.disabled_at.is_(None))
        )
    )
    if group_id is None:
        raise UnknownGroupException(group_name)

    membership_id = await database.execute(
        memberships.insert().values(user_id=user_id, group_id=group_id, status=status)
    )
    return membership_id


def eval_boolean_expression(
    expression: boolean.Expression, predicates: set[str]
) -> bool:
    if isinstance(expression, boolean.Symbol):
        logger.debug("SYM", expression.obj in predicates)
        return expression.obj in predicates
    elif isinstance(expression, boolean.AND):
        logger.debug("AND", expression.args)
        return all(eval_boolean_expression(arg, predicates) for arg in expression.args)
    elif isinstance(expression, boolean.OR):
        logger.debug("OR", expression.args)
        return any(eval_boolean_expression(arg, predicates) for arg in expression.args)
    elif isinstance(expression, boolean.NOT):
        logger.debug("NOT", expression.args)
        return not eval_boolean_expression(expression.args[0], predicates)
    elif isinstance(expression, boolean._TRUE):
        logger.debug("TRUE")
        return True
    elif isinstance(expression, boolean._FALSE):
        logger.debug("FALSE")
        return False
    else:
        raise Exception("unexpected error")


async def test_group_condition(user_id: int, condition: str) -> bool:
    await assert_user_exists(user_id)

    algebra = BooleanAlgebra()
    try:
        expression = algebra.parse(condition, simplify=False)
    except boolean.ParseError:
        raise InvalidExpressionException(condition)

    for symbol in expression.symbols:
        # TODO: test correct symbol format (zero or one colon)
        if ":" not in symbol.obj:
            symbol.obj += ":member"

    user_memberships = set(
        f"{membership_info.group}:{status.name}"
        for membership_info in await get_user_memberships(user_id)
        for status in GroupStatus
        if status.value <= membership_info.status.value
    )

    logger.debug(expression, user_memberships)
    return eval_boolean_expression(expression, user_memberships)
