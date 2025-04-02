import datetime

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import get_current_timezone
from pytest_django.asserts import assertTemplateUsed

from doctors.models import Appointment, Doctor

User = get_user_model()


@pytest.mark.django_db
class TestDoctorListView:
    def test_page_accessible(self, client):
        response = client.get(reverse('doctors:doctors_list'))
        assert response.status_code == 200

    def test_uses_correct_template(self, client):
        response = client.get(reverse('doctors:doctors_list'))
        assertTemplateUsed(response, 'doctors/doctors_list.html')

    def test_context_data(self, client, load_doctors_data):
        response = client.get(reverse('doctors:doctors_list'))
        doctors = Doctor.objects.all()
        assert list(response.context['doctors']) == list(
            doctors[:response.context['page_obj'].paginator.per_page]
        )


@pytest.mark.django_db
class TestDoctorDetailView:
    def test_returns_404_for_invalid_slug(self, client):
        invalid_slug = 'invalid_slug'
        url = reverse(
            'doctors:doctor_detail', kwargs={'slug': invalid_slug}
        )
        response = client.get(url)
        assert response.status_code == 404

    def test_page_accessible(self, client, load_doctors_data, first_doctor):
        response = client.get(reverse(
            'doctors:doctor_detail', kwargs={'slug': first_doctor.slug}
        ))
        assert response.status_code == 200

    def test_uses_correct_template(
            self, client, load_doctors_data, first_doctor
    ):
        response = client.get(reverse(
            'doctors:doctor_detail', kwargs={'slug': first_doctor.slug}
        ))
        assertTemplateUsed(response, 'doctors/doctor_detail.html')

    def test_context_data(self, client, load_doctors_data, first_doctor):
        response = client.get(reverse(
            'doctors:doctor_detail', kwargs={'slug': first_doctor.slug}
        ))
        assert response.context['doctor'] == first_doctor

    def test_doctor_detail_post(self, client, load_doctors_data, first_doctor):
        service = first_doctor.doctor_services.first()
        url = reverse(
            'doctors:doctor_detail',
            kwargs={'slug': first_doctor.slug}
        )
        response = client.post(url, {'service': service.pk})
        expected_url = reverse(
            'doctors:select_appointment_time',
            kwargs={'pk': service.pk}
        )
        assert response.status_code == 302
        assert response.url == expected_url

    def test_doctor_detail_post_invalid_form(
            self, client, load_doctors_data, first_doctor
    ):
        url = reverse(
            'doctors:doctor_detail',
            kwargs={'slug': first_doctor.slug}
        )
        response = client.post(url)
        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["form"].errors


@pytest.mark.django_db
class TestSelectAppointmentTime:
    def test_page_accessible(
            self, auth_client, load_doctors_data, first_doctorservice
    ):
        response = auth_client.get(reverse(
            'doctors:select_appointment_time',
            kwargs={'pk': first_doctorservice.pk}
        ))
        assert response.status_code == 200

    def test_uses_correct_template(
            self, auth_client, load_doctors_data, first_doctorservice
    ):
        response = auth_client.get(reverse(
            'doctors:select_appointment_time',
            kwargs={'pk': first_doctorservice.pk}
        ))
        assertTemplateUsed(response, 'doctors/select_appointment_time.html')

    def test_create_appointment_success(
        self, client, load_doctors_data, first_doctorservice
    ):
        user = User.objects.create_user(
            email="testauthuser2@example.com",
            password="testpass",
            gender='M',
            birth_date='2000-01-01',
            phone_number='+79991234567'
        )
        client.force_login(user)
        appointment_time = (
            datetime.datetime.now() + datetime.timedelta(days=1)
        ).strftime('%Y-%m-%d %H:%M')
        response = client.post(
            reverse(
                'doctors:select_appointment_time',
                kwargs={'pk': first_doctorservice.pk}
            ), {'datetime': appointment_time}
        )
        assert Appointment.objects.filter(
            user=user, service=first_doctorservice
        ).exists()
        appointment = Appointment.objects.get(
            user=user, service=first_doctorservice
        )
        assert response.status_code == 302
        assert response.url == reverse(
            'doctors:appointment_detail', kwargs={'pk': appointment.pk}
        )

    def test_create_invalid_appointment(
            self,
            client,
            load_doctors_data,
            first_doctorservice,
            first_appointment
    ):
        user = first_appointment.user
        client.force_login(user)

        appointment_time = first_appointment.appointment_time.astimezone(
            get_current_timezone()
        ).strftime('%Y-%m-%d %H:%M')

        initial_count = Appointment.objects.count()
        print(Appointment.objects.filter(
            user=user,
            service=first_doctorservice
        ))
        response = client.post(
            reverse(
                'doctors:select_appointment_time',
                kwargs={'pk': first_appointment.service.pk}
            ), {'datetime': appointment_time}
        )
        assert response.status_code == 200
        assert Appointment.objects.count() == initial_count

    def test_get_past_available_times(
        self, auth_client, load_doctors_data, first_doctorservice
    ):
        yesterday_date = (
            datetime.date.today() - datetime.timedelta(days=1)
        ).strftime('%Y-%m-%d')

        response = auth_client.get(
            reverse(
                'doctors:select_appointment_time',
                kwargs={'pk': first_doctorservice.pk}
            ),
            {'date': yesterday_date}
        )

        assert 'available_times' in response.context
        assert isinstance(response.context['available_times'], list)
        assert len(response.context['available_times']) == 0

    def test_get_today_available_times(
        self, auth_client, load_doctors_data, first_doctorservice
    ):
        today_datetime = datetime.datetime.today()
        response = auth_client.get(
            reverse(
                'doctors:select_appointment_time',
                kwargs={'pk': first_doctorservice.pk}
            )
        )
        start_hour = 9 if today_datetime.hour < 9 else today_datetime.hour + 1
        available_times_amount = max((18 - start_hour) * (
            60 / (first_doctorservice.duration.total_seconds() / 60)
        ), 0)
        assert 'available_times' in response.context
        assert isinstance(response.context['available_times'], list)
        assert (
            len(response.context['available_times'])
            == available_times_amount
        )

    @pytest.mark.django_db
    def test_get_all_available_times(
        self, auth_client, load_doctors_data, first_doctorservice
    ):
        tomorrow_date = (
            datetime.date.today() + datetime.timedelta(days=365)
        ).strftime('%Y-%m-%d')

        response = auth_client.get(
            reverse(
                'doctors:select_appointment_time',
                kwargs={'pk': first_doctorservice.pk}
            ),
            {'date': tomorrow_date}
        )
        available_times_amount = 9 * (
            60 / (first_doctorservice.duration.total_seconds() / 60)
        )
        assert 'available_times' in response.context
        assert isinstance(response.context['available_times'], list)
        assert (
            len(response.context['available_times']) == available_times_amount
        )
