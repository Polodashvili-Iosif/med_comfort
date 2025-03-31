from django.urls import path

from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctors_list'),
]
