from django.urls import path

from . import views

app_name = 'clinics'

urlpatterns = [
    path('', views.ClinicListView.as_view(), name='clinics_list'),
    path('<int:pk>/', views.ClinicDetailView.as_view(), name='clinic_detail')
]
