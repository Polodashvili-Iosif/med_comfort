import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestHomePage:
    def test_homepage_accessible_by_name(self, client: Client):
        response = client.get(reverse('main:index'))
        assert response.status_code == 200

    def test_homepage_uses_correct_template(self, client: Client):
        response = client.get(reverse('main:index'))
        assert response.templates[0].name == 'main/index.html'
