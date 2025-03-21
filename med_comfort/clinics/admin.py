from django.contrib import admin

from .models import Clinic, PhoneNumber


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')
    ordering = ('name',)


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'clinic', 'description')
    search_fields = ('number', 'clinic__name', 'description')
    list_filter = ('clinic',)
    ordering = ('clinic',)
