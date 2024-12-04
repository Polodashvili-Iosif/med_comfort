from django.shortcuts import get_object_or_404, render

from .models import Service, ServiceCategory


def services_list(request):
    service_catigories = ServiceCategory.objects.all()
    services = Service.objects.all()
    context = {
        'service_categories': service_catigories,
        'services': services,
    }
    return render(request, 'services/services_list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug)
    context = {
        'services': category.services.all(),
        'category': category
    }
    return render(request, 'services/category_detail.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    context = {
        'service': service
    }
    return render(request, 'services/service_detail.html', context)
