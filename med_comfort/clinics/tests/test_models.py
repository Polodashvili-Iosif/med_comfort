import pytest


@pytest.mark.django_db
class TestPhoneNumberModel:
    def test_clinic_str(self, load_clinics_data, first_clinic):
        assert str(first_clinic) == first_clinic.name


@pytest.mark.django_db
class TestServiceModel:
    def test_phone_number_str(self, load_clinics_data, first_phone_number):
        phone_number_international = first_phone_number.number.as_international
        assert str(first_phone_number) == phone_number_international
