from django.contrib import admin
from django.utils.html import format_html

from .models import (Appointment, Doctor, DoctorCategory, DoctorService,
                     Specialty)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DoctorCategory)
class DoctorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class DoctorServiceInline(admin.TabularInline):
    model = DoctorService
    autocomplete_fields = ["service"]
    min_num = 0


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'clinic',
        'experience',
        'patient_category',
        'preview_image'
    )
    list_filter = ('clinic', 'patient_category', 'specialty')
    search_fields = ('full_name', 'phone_number', 'email')
    filter_horizontal = ('specialty', 'doctor_category')
    readonly_fields = ['slug', 'full_name']
    inlines = [DoctorServiceInline]

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" '
                'style="border-radius:30%;" '
                'width=5% height=5% />',
                obj.image.url
            )
        return "-"

    preview_image.short_description = "Фото"


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'appointment_time')
