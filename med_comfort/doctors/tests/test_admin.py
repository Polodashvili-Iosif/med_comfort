import pytest
from django.contrib.admin.sites import site

from doctors.admin import DoctorAdmin
from doctors.models import Doctor


@pytest.mark.django_db
class TestDoctorAdmin:
    @pytest.fixture
    def admin_instance(self):
        return DoctorAdmin(Doctor, site)

    def test_preview_image_with_image(
            self, admin_instance, load_doctors_data, first_doctor
    ):

        expected_html = (
            f'<img src="{first_doctor.image.url}" '
            'style="border-radius:30%;" width=5% height=5% />'
        )
        assert admin_instance.preview_image(first_doctor) == expected_html

    def test_preview_image_without_image(
            self, admin_instance, load_doctors_data, first_doctor
    ):
        first_doctor.image = ""
        assert admin_instance.preview_image(first_doctor) == "-"
