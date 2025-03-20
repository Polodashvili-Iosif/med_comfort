from django.views.generic import DetailView, ListView

from .models import Clinic


class ClinicListView(ListView):
    model = Clinic
    context_object_name = 'clinics'
    template_name = "clinics/clinics_list.html"


class ClinicDetailView(DetailView):
    model = Clinic
    context_object_name = 'clinic'
    template_name = "clinics/clinic_detail.html"
