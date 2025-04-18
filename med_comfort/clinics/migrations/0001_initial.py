# Generated by Django 5.1.3 on 2025-03-20 14:55

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Электронная почта')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('opening_hours', models.CharField(max_length=50, verbose_name='Время работы')),
                ('image', models.ImageField(blank=True, null=True, upload_to='clinics/clinics_photos/', verbose_name='Фотография клиники')),
            ],
            options={
                'verbose_name': 'Клиника',
                'verbose_name_plural': 'Клиники',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='Описание')),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_numbers', to='clinics.clinic', verbose_name='Клиника')),
            ],
            options={
                'verbose_name': 'Номер телефона',
                'verbose_name_plural': 'Номера телефонов',
                'ordering': ['clinic'],
            },
        ),
    ]
