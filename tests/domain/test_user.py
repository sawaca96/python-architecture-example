import pytest

from app.models import FollowError, UnfollowError
from tests.utils import create_user_entity


def test_entity_identified_by_id() -> None:
    user = create_user_entity(id=1)
    same_user = create_user_entity(id=1)

    assert user == same_user


def test_user_cannot_follow_same_user_more_than_once() -> None:
    user_1 = create_user_entity(id=1)
    user_2 = create_user_entity(id=2, followings=[user_1])

    with pytest.raises(FollowError):
        user_2.follow(user_1)


def test_user_cannot_unfollow_user_have_not_followed() -> None:
    user_1 = create_user_entity(id=1)
    user_2 = create_user_entity(id=2)

    with pytest.raises(UnfollowError):
        user_2.unfollow(user_1)
