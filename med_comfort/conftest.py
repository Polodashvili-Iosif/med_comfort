import pytest
from django.core.management import call_command

from services.models import Service, ServiceCategory


@pytest.fixture
def load_service_data(db):
    call_command('loaddata', 'services_data.json')


@pytest.fixture
def first_service():
    return Service.objects.first()


@pytest.fixture
def first_category():
    return ServiceCategory.objects.first()
