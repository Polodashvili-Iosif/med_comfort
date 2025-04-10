from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

User = get_user_model()


@pytest.mark.django_db
class TestProfileView:
    def test_page_accessible(self, auth_client):
        response = auth_client.get(reverse('users:profile'))
        assert response.status_code == HTTPStatus.OK

    def test_redirect_not_auth_client(self, client):
        response = client.get(reverse('users:profile'))
        assert response.status_code == HTTPStatus.FOUND

    def test_uses_correct_template(self, auth_client):
        response = auth_client.get(reverse('users:profile'))
        assertTemplateUsed(response, 'users/profile.html')

    def test_context_data(self, client, load_users_data, first_user):
        client.force_login(first_user)
        response = client.get(reverse('users:profile'))
        assert response.context['user'] == first_user


@pytest.mark.django_db
class TestProfileUpdateView:
    def test_page_accessible(self, auth_client):
        response = auth_client.get(reverse('users:profile_edit'))
        assert response.status_code == HTTPStatus.OK

    def test_redirect_not_auth_client(self, client):
        response = client.get(reverse('users:profile_edit'))
        assert response.status_code == HTTPStatus.FOUND

    def test_uses_correct_template(self, auth_client):
        response = auth_client.get(reverse('users:profile_edit'))
        assertTemplateUsed(response, 'users/profile_edit.html')

    def test_context_data(self, client, load_users_data, first_user):
        client.force_login(first_user)
        response = client.get(reverse('users:profile'))
        assert response.context['user'] == first_user
