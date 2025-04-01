from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractUser):
    M = 'M'
    F = 'F'
    GENDER_CHOICES = [
        (M, 'Мужчина'),
        (F, 'Женщина'),
    ]

    username = None
    email = models.EmailField("Электронная почта", unique=True, blank=True)
    patronymic = models.CharField(
        'Отчество', max_length=150, blank=True, null=True
    )
    gender = models.CharField(
        'Пол', max_length=1, choices=GENDER_CHOICES
    )
    birth_date = models.DateField('Дата рождения')
    phone_number = PhoneNumberField('Номер телефона')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'gender', 'birth_date', 'phone_number'
    ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"
