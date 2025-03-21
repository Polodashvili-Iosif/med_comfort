import pytest
from django.core.management import call_command

from clinics.models import Clinic, PhoneNumber
from services.models import Service, ServiceCategory


@pytest.fixture
def load_service_data(db):
    call_command('loaddata', 'services_data.json')


@pytest.fixture
def load_clinics_data(db):
    call_command('loaddata', 'clinics_data.json')


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
