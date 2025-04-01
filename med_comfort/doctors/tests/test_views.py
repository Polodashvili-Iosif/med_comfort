import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from doctors.models import Doctor

User = get_user_model()


@pytest.mark.django_db
class TestDoctorListView:
    def test_page_accessible(self, client):
        response = client.get(reverse('doctors:doctors_list'))
        assert response.status_code == 200

    def test_uses_correct_template(self, client):
        response = client.get(reverse('doctors:doctors_list'))
        assertTemplateUsed(response, 'doctors/doctors_list.html')

    def test_context_data(self, client, load_doctors_data):
        response = client.get(reverse('doctors:doctors_list'))
        doctors = Doctor.objects.all()
        assert list(response.context['doctors']) == list(
            doctors[:response.context['page_obj'].paginator.per_page]
        )


@pytest.mark.django_db
class TestDoctorDetailView:
    def test_returns_404_for_invalid_slug(self, client):
        invalid_slug = 'invalid_slug'
        url = reverse(
            'doctors:doctor_detail', kwargs={'slug': invalid_slug}
        )
        response = client.get(url)
        assert response.status_code == 404

    def test_page_accessible(self, client, load_doctors_data, first_doctor):
        response = client.get(reverse(
            'doctors:doctor_detail', kwargs={'slug': first_doctor.slug}
        ))
        assert response.status_code == 200

    def test_uses_correct_template(
            self, client, load_doctors_data, first_doctor
    ):
        response = client.get(reverse(
            'doctors:doctor_detail', kwargs={'slug': first_doctor.slug}
        ))
        assertTemplateUsed(response, 'doctors/doctor_detail.html')

    def test_context_data(self, client, load_doctors_data, first_doctor):
        response = client.get(reverse(
            'doctors:doctor_detail', kwargs={'slug': first_doctor.slug}
        ))
        assert response.context['doctor'] == first_doctor
