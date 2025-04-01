from django.urls import path

from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctors_list'),
    path(
        '<slug:slug>/',
        views.DoctorDetailView.as_view(),
        name='doctor_detail'
    ),
    path(
        'select_appointment_time/<int:pk>/',
        views.select_appointment_time,
        name='select_appointment_time'
    ),
    path(
        'appointment/<int:pk>/',
        views.AppointmentView.as_view(),
        name='appointment_detail'
    ),
]
