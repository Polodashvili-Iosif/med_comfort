from django.shortcuts import render

from doctors.models import Doctor


def index(request):
    doctors = Doctor.objects.all()[:6]
    services = [doctor.services.first() for doctor in doctors]
    return render(request, 'main/index.html', {'services': services})
