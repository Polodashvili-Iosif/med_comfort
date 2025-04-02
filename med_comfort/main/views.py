from django.shortcuts import render

from clinics.models import Clinic
from doctors.models import Doctor
from services.models import Service


def index(request):
    doctors = Doctor.objects.all()[:6]
    popular_services = [doctor.services.first() for doctor in doctors]
    return render(
        request, 'main/index.html', {'popular_services': popular_services}
    )


def search(request):
    query = request.GET.get("q", "").strip()

    doctors = Doctor.objects.filter(
        full_name__icontains=query
    ) if query else Doctor.objects.none()
    services = Service.objects.filter(
        name__icontains=query
    ) if query else Service.objects.none()
    clinics = Clinic.objects.filter(
        name__icontains=query
    ) if query else Clinic.objects.none()

    return render(
        request, 'main/search.html', {
            'query': query,
            'doctors': doctors,
            'services': services,
            'clinics': clinics,
        }
    )
