import uuid

import pytest

from party_wall.authentication.user import User


def test_user_to_dict():
    given_data = {
        "id": uuid.uuid4(),
        "username": "someuser",
        "email": "someuser@somedomain.com",
        "first_name": "John",
        "last_name": "Doe",
        "authenticated": False,
        "superuser": False,
    }
    expected_data = given_data

    user = User(**given_data)
    actual_data = user.to_dict()

    assert actual_data == expected_data


@pytest.mark.parametrize(
    ["description", "given_id1", "given_id2", "expected_output"],
    [
        (
            "should return True if ids of users are equal",
            "03e00ea7-4352-404c-add7-a2c28af99d1c",
            "03e00ea7-4352-404c-add7-a2c28af99d1c",
            True,
        ),
        (
            "should return False if ids of users are different",
            "03e00ea7-4352-404c-add7-a2c28af99d1c",
            "75558781-82b2-4dca-914b-b558848eadc1",
            False,
        ),
    ],
)
def test_user_equality(description, given_id1, given_id2, expected_output):
    given_common_data = {
        "username": "someuser",
        "email": "someuser@somedomain.com",
        "first_name": "John",
        "last_name": "Doe",
        "authenticated": False,
        "superuser": False,
    }
    given_user1 = User(id=given_id1, **given_common_data)
    given_user2 = User(id=given_id2, **given_common_data)

    actual_output = given_user1 == given_user2

    assert actual_output is expected_output


@pytest.mark.parametrize(
    ["description", "given_id1", "given_id2", "expected_output"],
    [
        (
            "should return False if ids of users are equal",
            "03e00ea7-4352-404c-add7-a2c28af99d1c",
            "03e00ea7-4352-404c-add7-a2c28af99d1c",
            False,
        ),
        (
            "should return True if ids of users are different",
            "03e00ea7-4352-404c-add7-a2c28af99d1c",
            "75558781-82b2-4dca-914b-b558848eadc1",
            True,
        ),
    ],
)
def test_user_inequality(description, given_id1, given_id2, expected_output):
    given_common_data = {
        "username": "someuser",
        "email": "someuser@somedomain.com",
        "first_name": "John",
        "last_name": "Doe",
        "authenticated": False,
        "superuser": False,
    }
    given_user1 = User(id=given_id1, **given_common_data)
    given_user2 = User(id=given_id2, **given_common_data)

    actual_output = given_user1 != given_user2

    assert actual_output is expected_output
