from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserAdmin(UserAdmin):
    add_form_template = None
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": (
            "first_name",
            "last_name",
            "patronymic",
            "gender",
            "birth_date",
            "phone_number"
        )}),
        (
            _("Permissions"), {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                )
            }
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("usable_password", "password1", "password2"),
            }
        ),
    )
    list_display = (
        'email', 'first_name', 'last_name', 'is_staff'
    )
    search_fields = ("first_name", "last_name", "email")
    ordering = ('email',)
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, CustomUserAdmin)
