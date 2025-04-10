from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from clinics.models import Clinic


@pytest.mark.django_db
class TestClinicListView:
    def test_page_accessible(self, client):
        response = client.get(reverse('clinics:clinics_list'))
        assert response.status_code == HTTPStatus.OK

    def test_uses_correct_template(self, client):
        response = client.get(reverse('clinics:clinics_list'))
        assertTemplateUsed(response, 'clinics/clinics_list.html')

    def test_context_data(self, client, load_clinics_data):
        response = client.get(reverse('clinics:clinics_list'))
        clinics = Clinic.objects.all()
        assert list(response.context['clinics']) == list(clinics)


@pytest.mark.django_db
class TestServiceDetailView:
    def test_returns_404_for_invalid_pk(self, client):
        invalid_pk = 0
        url = reverse(
            'clinics:clinic_detail', kwargs={'pk': invalid_pk}
        )
        response = client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_page_accessible(self, client, load_clinics_data, first_clinic):
        response = client.get(reverse(
            'clinics:clinic_detail', kwargs={'pk': first_clinic.pk}
        ))
        assert response.status_code == HTTPStatus.OK

    def test_uses_correct_template(
            self, client, load_clinics_data, first_clinic
    ):
        response = client.get(reverse(
            'clinics:clinic_detail', kwargs={'pk': first_clinic.pk}
        ))
        assertTemplateUsed(response, 'clinics/clinic_detail.html')

    def test_context_data(self, client, load_clinics_data, first_clinic):
        response = client.get(reverse(
            'clinics:clinic_detail', kwargs={'pk': first_clinic.pk}
        ))
        assert response.context['clinic'] == first_clinic
