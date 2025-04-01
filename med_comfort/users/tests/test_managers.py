import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserManager:
    def test_create_user(self):
        user = User.objects.create_user(
            email="user@example.com",
            password="password123",
            gender='M',
            birth_date='2000-01-01',
            phone_number='+79991234567'
        )
        assert user.email == "user@example.com"
        assert user.check_password("password123")
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_user_without_email(self):
        with pytest.raises(
            ValueError, match="У пользователя должен быть email"
        ):
            User.objects.create_user(
                email="",
                password="password123",
                gender='M',
                birth_date='2000-01-01',
                phone_number='+79991234567'
            )

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            gender='M',
            birth_date='2000-01-01',
            phone_number='+79991234567'
        )
        assert admin_user.email == "admin@example.com"
        assert admin_user.check_password("adminpassword")
        assert admin_user.is_active
        assert admin_user.is_staff
        assert admin_user.is_superuser

    def test_create_superuser_is_staff_and_superuser_true(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            gender='M',
            birth_date='2000-01-01',
            phone_number='+79991234567'
        )
        assert admin_user.is_staff
        assert admin_user.is_superuser
