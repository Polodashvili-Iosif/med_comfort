import pytest


@pytest.mark.django_db
class TestUserModel:
    def test_user_str(self, load_users_data, first_user):
        assert (
            str(first_user)
            == (
                f"{first_user.last_name} "
                f"{first_user.first_name} "
                f"{first_user.patronymic or ''}"
            ).strip()
        )
