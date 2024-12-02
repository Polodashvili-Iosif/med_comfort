from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='services_list'),
    path(
        'category/<slug:slug>/', views.category_detail, name='category_detail'
    )
]
