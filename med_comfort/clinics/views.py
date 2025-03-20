from django.views.generic import ListView

from .models import Clinic


class ClinicListView(ListView):
    model = Clinic
    context_object_name = 'clinics'
    template_name = "clinics/clinics_list.html"
