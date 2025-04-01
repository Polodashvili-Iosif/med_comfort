import pytest
from django.db.models import Q

from doctors.filters import DoctorFilter
from doctors.models import Doctor


@pytest.mark.django_db
def test_doctor_filter_search(load_doctors_data):
    doctor = Doctor.objects.first()
    search_value = doctor.first_name[:3]

    filtered_queryset = DoctorFilter(
        {"search": search_value}, queryset=Doctor.objects.all()
    ).qs
    assert doctor in filtered_queryset

    expected_queryset = Doctor.objects.filter(
        Q(first_name__icontains=search_value)
        | Q(last_name__icontains=search_value)
        | Q(patronymic__icontains=search_value)
        | Q(specialty__name__icontains=search_value)
    ).distinct()
    assert set(filtered_queryset) == set(expected_queryset)
