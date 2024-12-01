from django.shortcuts import render

from .models import Service, ServiceCategory


def services_list(request):
    service_catigories = ServiceCategory.objects.all()
    services = Service.objects.all()
    context = {
        'service_categories': service_catigories,
        'services': services,
    }
    return render(request, 'services/services_list.html', context)
