from django_filters.views import FilterView

from .filters import DoctorFilter
from .models import Doctor


class DoctorListView(FilterView):
    model = Doctor
    template_name = 'doctors/doctors_list.html'
    context_object_name = 'doctors'
    filterset_class = DoctorFilter
    paginate_by = 8
