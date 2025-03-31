import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from clinics.models import Clinic, PhoneNumber
from doctors.models import (Appointment, Doctor, DoctorCategory, DoctorService,
                            Specialty)
from services.models import Service, ServiceCategory

User = get_user_model()


@pytest.fixture
def auth_client(db, client):
    user = User.objects.create_user(
        username="testauthuser", password="testpass"
    )
    client.force_login(user)
    return client


@pytest.fixture
def load_service_data(db):
    call_command('loaddata', 'services_data.json')


@pytest.fixture
def load_clinics_data(db):
    call_command('loaddata', 'clinics_data.json')


@pytest.fixture
def load_doctors_data(db):
    User.objects.create_user(
        username="testuser", password="testpass"
    )
    call_command('loaddata', 'services_data.json')
    call_command('loaddata', 'clinics_data.json')
    call_command('loaddata', 'doctors_data.json')


@pytest.fixture
def first_service():
    return Service.objects.first()


@pytest.fixture
def first_category():
    return ServiceCategory.objects.first()


@pytest.fixture
def first_clinic():
    return Clinic.objects.first()


@pytest.fixture
def first_phone_number():
    return PhoneNumber.objects.first()


@pytest.fixture
def first_doctor():
    return Doctor.objects.first()


@pytest.fixture
def first_doctor_category():
    return DoctorCategory.objects.first()


@pytest.fixture
def first_specialty():
    return Specialty.objects.first()


@pytest.fixture
def first_doctorservice():
    return DoctorService.objects.first()


@pytest.fixture
def first_appointment():
    return Appointment.objects.first()
