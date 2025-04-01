from django import forms

from .models import DoctorService


class DoctorServiceForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=DoctorService.objects.all(),
        widget=forms.RadioSelect,
        label="Выберите услугу",
    )
