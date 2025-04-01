from django.urls import path

from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctors_list'),
    path(
        '<slug:slug>/',
        views.DoctorDetailView.as_view(),
        name='doctor_detail'
    )
]
