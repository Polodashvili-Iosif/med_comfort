import django_filters
from django.db.models import Q

from .models import Doctor, Specialty


class DoctorFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        label='Поиск по ФИО или специальности',
        method='filter_by_name_or_specialty',
    )

    class Meta:
        model = Doctor
        fields = [
            "patient_category", "clinic", "specialty", "doctor_category"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "specialty" in self.filters:
            self.filters["specialty"].queryset = Specialty.objects.filter(
                doctors__isnull=False
            ).distinct()

        for field_name, filter_field in self.filters.items():
            if isinstance(
                filter_field, django_filters.ModelMultipleChoiceFilter
            ):
                filter_field.conjoined = True

    def filter_by_name_or_specialty(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value)
            | Q(specialty__name__icontains=value)
        ).distinct()
