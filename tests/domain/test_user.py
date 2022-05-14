from tests.utils import create_user_entity


def test_entity_identified_by_id() -> None:
    user = create_user_entity(id=1)
    same_user = create_user_entity(id=1)

    assert user == same_user
