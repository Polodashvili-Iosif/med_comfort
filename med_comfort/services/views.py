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


def category_detail(request, pk):
    category = get_object_or_404(ServiceCategory, id=pk)
    context = {
        'services': category.services.all(),
        'category': category
    }
    return render(request, 'services/category_detail.html', context)
