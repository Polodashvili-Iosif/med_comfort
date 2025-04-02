from django.shortcuts import get_object_or_404, render

from doctors.models import Doctor

from .models import Service, ServiceCategory


def services_list(request):
    service_categories = ServiceCategory.objects.filter(
        services__doctor_services__isnull=False
    ).distinct()
    services = Service.objects.filter(doctor_services__isnull=False).distinct()
    doctors = Doctor.objects.all()[:6]
    popular_services = [doctor.services.first() for doctor in doctors]
    context = {
        'service_categories': service_categories,
        'services': services,
        'popular_services': popular_services,
    }
    return render(request, 'services/services_list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug)
    services = category.services.filter(
        doctor_services__isnull=False
    ).distinct()
    context = {
        'services': services,
        'category': category
    }
    return render(request, 'services/category_detail.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    doctors = Doctor.objects.filter(services=service)
    context = {
        'service': service,
        'doctors': doctors,
    }
    return render(request, 'services/service_detail.html', context)
