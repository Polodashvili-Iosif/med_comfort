"""
Module defines the application configuration for the 'main' application.
"""
from django.apps import AppConfig


class MainConfig(AppConfig):
    """
    Configuration class for the 'main' application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
