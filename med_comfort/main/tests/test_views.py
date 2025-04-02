import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from clinics.models import Clinic
from doctors.models import Doctor
from services.models import Service

User = get_user_model()


@pytest.mark.django_db
class TestIndexePage:
    def test_page_accessible(self, client):
        response = client.get(reverse('main:index'))
        assert response.status_code == 200

    def test_uses_correct_template(self, client):
        response = client.get(reverse('main:index'))
        assert response.templates[0].name == 'main/index.html'


@pytest.mark.django_db
class TestSearchView:
    def test_page_accessible(self, client):
        response = client.get(reverse('main:search'))
        assert response.status_code == 200

    def test_uses_correct_template(self, client):
        response = client.get(reverse('main:search'))
        assertTemplateUsed(response, 'main/search.html')

    def test_context_data(self, client, load_doctors_data):
        query = 'Ко'
        response = client.get(reverse('main:search'), {'q': query})
        doctors = Doctor.objects.filter(
            full_name__icontains=query
        )
        services = Service.objects.filter(
            name__icontains=query, doctor_services__isnull=False
        ).distinct()
        clinics = Clinic.objects.filter(
            name__icontains=query
        )

        # assert response.context == ''
        assert response.context['query'] == query
        assert list(response.context['doctors']) == list(doctors)
        assert list(response.context['services']) == list(services)
        assert list(response.context['clinics']) == list(clinics)
