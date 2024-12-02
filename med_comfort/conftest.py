import pytest
from django.core.management import call_command


@pytest.fixture
def load_service_data(db):
    call_command('loaddata', 'services_data.json')
