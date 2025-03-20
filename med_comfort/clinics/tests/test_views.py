import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from clinics.models import Clinic


@pytest.mark.django_db
class TestClinicListView:
    def test_page_accessible(self, client):
        response = client.get(reverse('clinics:clinics_list'))
        assert response.status_code == 200

    def test_uses_correct_template(self, client):
        response = client.get(reverse('clinics:clinics_list'))
        assertTemplateUsed(response, 'clinics/clinics_list.html')

    def test_context_data(self, client, load_service_data):
        response = client.get(reverse('clinics:clinics_list'))
        clinics = Clinic.objects.all()
        assert list(response.context['clinics']) == list(clinics)
