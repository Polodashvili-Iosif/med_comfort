from copy import deepcopy

import pytest
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from unidecode import unidecode

from doctors.models import Appointment


@pytest.mark.django_db
@pytest.mark.parametrize(
    "instance, expected",
    [
        ("first_specialty", "name"),
        ("first_doctor_category", "name"),
        ("first_doctor", "full_name"),
    ],
)
def test_model_str(instance, expected, request, load_doctors_data):
    model_instance = request.getfixturevalue(instance)
    assert str(model_instance) == getattr(model_instance, expected)


@pytest.mark.django_db
def test_doctor_full_name_updates_on_save(load_doctors_data, first_doctor):
    old_full_name = first_doctor.full_name

    first_doctor.first_name = "Иван"
    first_doctor.last_name = "Петров"
    first_doctor.patronymic = "Сергеевич"
    first_doctor.save()

    first_doctor.refresh_from_db()

    assert first_doctor.full_name != old_full_name
    assert first_doctor.full_name == "Петров Иван Сергеевич"


@pytest.mark.django_db
def test_doctor_slug_updates_on_save(load_doctors_data, first_doctor):
    old_slug = first_doctor.slug

    first_doctor.first_name = "Иван"
    first_doctor.last_name = "Петров"
    first_doctor.patronymic = "Сергеевич"
    first_doctor.save()
    first_doctor.refresh_from_db()

    expected_slug = slugify(unidecode(first_doctor.full_name))
    assert first_doctor.slug != old_slug
    assert first_doctor.slug == expected_slug


@pytest.mark.django_db
def test_doctor_slug_uniqueness(load_doctors_data, first_doctor):
    duplicate_doctor = deepcopy(first_doctor)
    duplicate_doctor.pk = None
    duplicate_doctor.save()

    assert duplicate_doctor.slug == f'{first_doctor.slug}-2'


@pytest.mark.django_db
def test_overlapping_appointment(load_doctors_data, first_appointment):
    with pytest.raises(ValidationError):
        Appointment.objects.create(
            user=first_appointment.user,
            service=first_appointment.service,
            appointment_time=first_appointment.appointment_time
        )
