from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Clinics(models.Model):
    name = models.CharField('Название', max_length=255)
    address = models.CharField('Адрес', max_length=255)
    email = models.EmailField(
        verbose_name="Электронная почта", blank=True, null=True
    )
    description = models.TextField(
        verbose_name="Описание", blank=True, null=True
    )

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиники'
        ordering = ['name']

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    clinic = models.ForeignKey(
        Clinics,
        on_delete=models.CASCADE,
        related_name='phone_numbers',
        verbose_name='Клиника'
    )
    number = PhoneNumberField("Номер телефона")
    description = models.CharField(
        'Описание',
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Номер телефона'
        verbose_name_plural = 'Номера телефонов'
        ordering = ['clinic']

    def __str__(self):
        return self.number.as_international
