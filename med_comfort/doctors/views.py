import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import make_aware
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from .filters import DoctorFilter
from .forms import DoctorServiceForm
from .models import Appointment, Doctor, DoctorService


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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            service_pk = form.cleaned_data["service"].pk
            return HttpResponseRedirect(reverse(
                'doctors:select_appointment_time',
                kwargs={'pk': service_pk}
            ))
        return self.form_invalid(form)


@login_required
def select_appointment_time(request, pk):
    service = get_object_or_404(DoctorService, pk=pk)
    today_datetime = datetime.datetime.today()

    selected_date = request.GET.get(
        'date',
        today_datetime.strftime('%Y-%m-%d')
    )
    selected_datetime = datetime.datetime.strptime(selected_date, '%Y-%m-%d')

    if selected_datetime.date() == today_datetime.date():
        start_time = datetime.time(max(9, today_datetime.hour + 1), 0)
    elif selected_datetime.date() < today_datetime.date():
        start_time = datetime.time(18, 0)
    else:
        start_time = datetime.time(9, 0)
    end_time = datetime.time(18, 0)
    service_duration = service.duration

    available_times = []
    selected_time = make_aware(
        datetime.datetime.combine(selected_datetime, start_time)
    )
    while selected_time.time() < end_time:
        appointment_end = selected_time + service_duration
        service_duration = service.duration
        appointment_end = selected_time + service_duration

        overlapping_appointments = Appointment.objects.filter(
            service__doctor=service.doctor,
            appointment_time__gte=selected_time,
            appointment_time__lt=appointment_end,
        )

        if not overlapping_appointments.exists():
            available_times.append(selected_time.time())
        selected_time += service_duration

    if request.method == 'POST':
        selected_time_str = request.POST.get('datetime')
        try:
            appointment_datetime = make_aware(
                datetime.datetime.strptime(selected_time_str, '%Y-%m-%d %H:%M')
            )
            appointment = Appointment(
                user=request.user,
                service=service,
                appointment_time=appointment_datetime
            )
            appointment.save()

            return redirect('doctors:appointment_detail', pk=appointment.pk)
        except ValidationError:
            pass

    return render(
        request,
        'doctors/select_appointment_time.html',
        {
            'service': service,
            'available_times': available_times,
            'selected_date': selected_date
        }
    )


class AppointmentView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appointment
    template_name = 'doctors/appointment_detail.html'
    context_object_name = 'appointment'

    def test_func(self):
        appointment = self.get_object()
        return appointment.user == self.request.user

    def handle_no_permission(self):
        return redirect("users:profile")
