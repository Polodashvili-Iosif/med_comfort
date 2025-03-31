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
