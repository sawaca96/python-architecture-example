from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import UserRepositoryImpl
from tests.utils import insert_user


async def test_create_user_ok(session: AsyncSession) -> None:
    # given
    repo = UserRepositoryImpl(session)

    # when
    user = await repo.create(
        username="jake",
        email="jake@jake.jake",
        password="password",
    )

    # then
    result: CursorResult = await session.execute('SELECT * FROM "user"')
    row = dict(result.one())
    assert user.id == row["id"]


async def test_get_user_by_id(session: AsyncSession) -> None:
    # given
    user_a = await insert_user(session, username="jake", email="jake@jake.jake")
    user_b = await insert_user(session, username="jone", email="jone@jone.jone")
    user_a.follow(user_b.id)
    repo = UserRepositoryImpl(session)
    await repo.follow(user_a)

    # when
    user = await repo.get_by_id(user_a.id)

    # then
    assert user.id == user_a.id
    assert user.followings[0] == user_b.id


async def test_update_user(session: AsyncSession) -> None:
    # given
    given_user = await insert_user(session, username="jake", email="jake@jake.jake")
    repo = UserRepositoryImpl(session)

    # when
    user = await repo.update(
        user_id=given_user.id,
        username="new_username",
        email="new_email@example.com",
        bio="I like to skateboard",
        image="https://i.stack.imgur.com/xHWG8.jpg",
    )

    # then
    assert user.username == "new_username"
    assert user.email == "new_email@example.com"
    assert user.bio == "I like to skateboard"
    assert user.image == "https://i.stack.imgur.com/xHWG8.jpg"


async def test_follow(session: AsyncSession) -> None:
    # given
    user_a = await insert_user(session, username="jake", email="jake@jake.jake")
    user_b = await insert_user(session, username="jone", email="jone@jone.jone")
    user_c = await insert_user(session, username="jane", email="jane@jane.jane")
    user_a.follow(user_c.id)
    repo = UserRepositoryImpl(session)
    await repo.follow(user_a)
    user_a.follow(user_b.id)

    # when
    is_success = await repo.follow(user_a)

    # then
    assert is_success is True
    result = await session.execute(
        "SELECT following_id FROM follower_x_following"
        " WHERE follower_id = :follower_id",
        {"follower_id": user_a.id},
    )
    rows = [dict(r) for r in result.all()]
    assert {user_b.id, user_c.id} == {r["following_id"] for r in rows}


async def test_unfollow(session: AsyncSession) -> None:
    # given
    user_a = await insert_user(session, username="jake", email="jake@jake.jake")
    user_b = await insert_user(session, username="jone", email="jone@jone.jone")
    user_c = await insert_user(session, username="jane", email="jane@jane.jane")
    user_a.follow(user_c.id)
    user_a.follow(user_b.id)
    repo = UserRepositoryImpl(session)
    await repo.follow(user_a)

    # when
    user_a.unfollow(user_b.id)
    is_success = await repo.unfollow(user_a)

    # then
    assert is_success is True
    result = await session.execute(
        "SELECT following_id FROM follower_x_following"
        " WHERE follower_id = :follower_id",
        {"follower_id": user_a.id},
    )
    rows = [dict(r) for r in result.all()]
    assert {user_c.id} == {r["following_id"] for r in rows}
