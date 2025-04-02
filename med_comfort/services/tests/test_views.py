import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from services.models import Service, ServiceCategory


@pytest.mark.django_db
class TestServiceListView:
    def test_page_accessible(self, client):
        response = client.get(reverse('services:services_list'))
        assert response.status_code == 200

    def test_uses_correct_template(self, client):
        response = client.get(reverse('services:services_list'))
        assertTemplateUsed(response, 'services/services_list.html')

    def test_context_data(self, client, load_service_data):
        response = client.get(reverse('services:services_list'))
        services = Service.objects.filter(
            doctor_services__isnull=False
        ).distinct()
        service_categories = ServiceCategory.objects.filter(
            services__doctor_services__isnull=False
        ).distinct()

        assert list(response.context['services']) == list(services)
        assert (
            list(response.context['service_categories'])
            == list(service_categories)
        )


@pytest.mark.django_db
class TestCategoryDetailView:
    def test_returns_404_for_invalid_slug(self, client):
        invalid_slug = "non-existent-category"
        url = reverse(
            'services:category_detail', kwargs={'slug': invalid_slug}
        )
        response = client.get(url)
        assert response.status_code == 404

    def test_page_accessible(self, client, load_service_data, first_category):
        response = client.get(reverse(
            'services:category_detail', kwargs={'slug': first_category.slug}
        ))
        assert response.status_code == 200

    def test_uses_correct_template(
            self, client, load_service_data, first_category
    ):
        response = client.get(reverse(
            'services:category_detail', kwargs={'slug': first_category.slug}
        ))
        assertTemplateUsed(response, 'services/category_detail.html')

    def test_context_data(self, client, load_service_data, first_category):
        response = client.get(reverse(
            'services:category_detail', kwargs={'slug': first_category.slug}
        ))
        services = Service.objects.filter(
            doctor_services__isnull=False
        ).distinct()

        assert list(response.context['services']) == list(services)


@pytest.mark.django_db
class TestServiceDetailView:
    def test_returns_404_for_invalid_slug(self, client):
        invalid_slug = "non-existent-service"
        url = reverse(
            'services:service_detail', kwargs={'slug': invalid_slug}
        )
        response = client.get(url)
        assert response.status_code == 404

    def test_page_accessible(self, client, load_service_data, first_service):
        response = client.get(reverse(
            'services:service_detail', kwargs={'slug': first_service.slug}
        ))
        assert response.status_code == 200

    def test_uses_correct_template(
            self, client, load_service_data, first_service
    ):
        response = client.get(reverse(
            'services:service_detail', kwargs={'slug': first_service.slug}
        ))
        assertTemplateUsed(response, 'services/service_detail.html')

    def test_context_data(self, client, load_service_data, first_service):
        response = client.get(reverse(
            'services:service_detail', kwargs={'slug': first_service.slug}
        ))
        assert response.context['service'] == first_service
