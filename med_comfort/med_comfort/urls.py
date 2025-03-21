"""
URL configuration for med_comfort project.
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def page_not_found_handler(request, exception=None):
    if request.path.startswith('/services/category/'):
        return render(request, 'services/404_category.html', status=404)
    if request.path.startswith('/services/'):
        return render(request, 'services/404_services.html', status=404)
    return render(request, '404.html', status=404)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('services/', include('services.urls')),
    path('clinics/', include('clinics.urls')),
]

handler404 = page_not_found_handler
