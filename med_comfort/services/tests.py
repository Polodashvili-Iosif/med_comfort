import pytest
from django.test import Client
from django.urls import reverse

from services.models import Service, ServiceCategory


@pytest.mark.django_db
class TestServiceListView:
    def test_service_list_page_accessible_by_name(self, client: Client):
        response = client.get(reverse('services:services_list'))
        assert response.status_code == 200

    def test_service_list_uses_correct_template(self, client: Client):
        response = client.get(reverse('services:services_list'))
        assert response.templates[0].name == 'services/services_list.html'

    def test_service_list_context_data(
        self, client: Client, load_service_data
    ):
        response = client.get(reverse('services:services_list'))
        services = Service.objects.all()
        service_categories = ServiceCategory.objects.all()

        assert list(response.context['services']) == list(services)
        assert (
            list(response.context['service_categories'])
            == list(service_categories)
        )
