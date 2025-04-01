from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from .filters import DoctorFilter
from .forms import DoctorServiceForm
from .models import Doctor, DoctorService


class DoctorListView(FilterView):
    model = Doctor
    template_name = 'doctors/doctors_list.html'
    context_object_name = 'doctors'
    filterset_class = DoctorFilter
    paginate_by = 8


class DoctorDetailView(FormMixin, DetailView):
    model = Doctor
    template_name = 'doctors/doctor_detail.html'
    context_object_name = 'doctor'
    form_class = DoctorServiceForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['service'].queryset = DoctorService.objects.filter(
            doctor=self.get_object()
        )
        return form
