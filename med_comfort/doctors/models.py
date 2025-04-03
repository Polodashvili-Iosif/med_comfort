from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from unidecode import unidecode

from clinics.models import Clinic
from services.models import Service

User = get_user_model()


class Specialty(models.Model):
    name = models.CharField('Специальность', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ['name']

    def __str__(self):
        return self.name


class DoctorCategory(models.Model):
    name = models.CharField('Категория врача', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Категория врача'
        verbose_name_plural = 'Категории врачей'
        ordering = ['name']

    def __str__(self):
        return self.name


class Doctor(models.Model):
    ADULT = 'adult'
    CHILD = 'child'
    BOTH = 'both'
    PATIENT_CATEGORIES = [
        (ADULT, 'Взрослый'),
        (CHILD, 'Детский'),
        (BOTH, 'Взрослый и детский'),
    ]
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    patronymic = models.CharField(
        'Отчество', max_length=30, blank=True, null=True
    )
    full_name = models.CharField(
        'Полное имя', max_length=100, editable=False, db_index=True
    )
    phone_number = PhoneNumberField('Номер телефона', blank=True, null=True)
    email = models.EmailField('Электронная почта', blank=True, null=True)
    patient_category = models.CharField(
        'Категория пациентов',
        max_length=10,
        choices=PATIENT_CATEGORIES,
        db_index=True
    )
    specialty = models.ManyToManyField(
        Specialty,
        verbose_name='Специальности врача',
        related_name='doctors',
        blank=True
    )
    doctor_category = models.ManyToManyField(
        DoctorCategory,
        verbose_name='Категории врача',
        related_name='doctors',
        blank=True
    )
    clinic = models.ForeignKey(
        Clinic,
        verbose_name='Клиника',
        on_delete=models.SET_NULL,
        related_name='doctors',
        blank=True,
        null=True
    )
    services = models.ManyToManyField(
        Service,
        through='DoctorService',
        verbose_name="Оказываемые услуги"
    )
    education = models.TextField('Образование')
    experience = models.PositiveIntegerField('Опыт работы (лет)')
    image = models.ImageField(
        'Фото', upload_to='doctors/images/', blank=True, null=True
    )
    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['last_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = (
            f"{self.last_name} {self.first_name} {self.patronymic or ''}"
        ).strip()
        base_slug = slugify(unidecode(self.full_name))
        unique_slug = base_slug
        num = 1
        while Doctor.objects.filter(
                slug=unique_slug
        ).exclude(pk=self.pk).exists():
            num += 1
            unique_slug = f"{base_slug}-{num}"
        self.slug = unique_slug
        super().save(*args, **kwargs)


class DoctorService(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name="Врач",
        related_name="doctor_services"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name="Услуга",
        related_name="doctor_services"
    )
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)
    duration = models.DurationField(
        "Длительность услуги",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Услуга врача"
        verbose_name_plural = "Услуги врачей"
        unique_together = ("doctor", "service")

    def __str__(self):
        return f"{self.doctor} - {self.service} ({self.price} руб.)"


class Appointment(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (PENDING, 'Ожидание подтверждения'),
        (CONFIRMED, 'Подтверждена'),
        (CANCELLED, 'Отменена'),
        (COMPLETED, 'Завершена'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='appointments'
    )
    service = models.ForeignKey(
        'DoctorService',
        related_name='appointments',
        on_delete=models.CASCADE,
        verbose_name='Услуга врача'
    )
    appointment_time = models.DateTimeField('Дата и время записи')
    status = models.CharField(
        'Статус', max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    created_at = models.DateTimeField(
        'Дата и время создания', auto_now_add=True
    )

    class Meta:
        verbose_name = "Запись на приём"
        verbose_name_plural = "Записи на приём"
        unique_together = ('service', 'appointment_time')

    def clean(self):
        service_duration = self.service.duration
        appointment_end = self.appointment_time + service_duration

        overlapping_appointments = Appointment.objects.filter(
            service__doctor=self.service.doctor
        ).exclude(pk=self.pk).filter(
            appointment_time__lt=appointment_end,
            appointment_time__gte=self.appointment_time
        )

        overlapping_existing = Appointment.objects.filter(
            service__doctor=self.service.doctor
        ).exclude(pk=self.pk).filter(
            appointment_time__lt=self.appointment_time,
            appointment_time__gte=(
                self.appointment_time
                - F('service__duration')
            )
        )

        if overlapping_appointments.exists() or overlapping_existing.exists():
            raise ValidationError(
                "Это время уже занято. Выберите другой слот."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.service} - "
            f"{self.appointment_time.strftime('%d.%m.%Y %H:%M')}"
        )
