import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestServiceListView:
    def test_service_list_page_accessible_by_name(self, client: Client):
        response = client.get(reverse('services:services_list'))
        assert response.status_code == 200
