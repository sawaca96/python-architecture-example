from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import UserRepositoryImpl


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
    actual_user = await repo.get_by_id(user.id)
    assert user.id == actual_user.id


async def test_get_user_by_id(session: AsyncSession) -> None:
    # given
    repo = UserRepositoryImpl(session)
    user = await repo.create(
        username="jake",
        email="jake@jake.jake",
        password="password",
    )

    # when
    actual_user = await repo.get_by_id(user.id)

    # then
    assert actual_user.id == user.id


async def test_update_user(session: AsyncSession) -> None:
    # given
    repo = UserRepositoryImpl(session)
    user = await repo.create(
        username="jake",
        email="jake@jake.jake",
        password="password",
    )

    # when
    updated_user = user.copy(
        update={
            "username": "new_username",
            "email": "new_email@example.com",
            "bio": "I like to skateboard",
            "image": "https://i.stack.imgur.com/xHWG8.jpg",
        },
    )
    await repo.update(updated_user)

    # then
    actual_user = await repo.get_by_id(user.id)
    assert actual_user.username == "new_username"
    assert actual_user.email == "new_email@example.com"
    assert actual_user.bio == "I like to skateboard"
    assert actual_user.image == "https://i.stack.imgur.com/xHWG8.jpg"


async def test_follow(session: AsyncSession) -> None:
    # given
    repo = UserRepositoryImpl(session)
    user_a = await repo.create(
        username="jake",
        email="jake@jake.jake",
        password="password",
    )
    user_b = await repo.create(
        username="jone",
        email="jone@jone.jone",
        password="password",
    )
    user_c = await repo.create(
        username="jane",
        email="jane@jane.jane",
        password="password",
    )

    # when
    await repo.follow(user_a, user_c)
    await repo.follow(user_a, user_b)

    # then
    result = await session.execute(
        "SELECT following_id FROM follower_x_following"
        " WHERE follower_id = :follower_id",
        {"follower_id": user_a.id},
    )
    rows = [dict(r) for r in result.all()]
    assert {user_b.id, user_c.id} == {r["following_id"] for r in rows}


async def test_unfollow(session: AsyncSession) -> None:
    # given
    repo = UserRepositoryImpl(session)
    user_a = await repo.create(
        username="jake",
        email="jake@jake.jake",
        password="password",
    )
    user_b = await repo.create(
        username="jone",
        email="jone@jone.jone",
        password="password",
    )
    user_c = await repo.create(
        username="jane",
        email="jane@jane.jane",
        password="password",
    )
    await repo.follow(user_a, user_b)
    await repo.follow(user_a, user_c)

    # when
    await repo.unfollow(user_a, user_b)

    # then
    result = await session.execute(
        "SELECT following_id FROM follower_x_following"
        " WHERE follower_id = :follower_id",
        {"follower_id": user_a.id},
    )
    rows = [dict(r) for r in result.all()]
    assert {user_c.id} == {r["following_id"] for r in rows}
