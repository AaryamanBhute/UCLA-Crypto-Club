from __future__ import unicode_literals
from django.apps import AppConfig
import decimal


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self) -> None:
        decimal.getcontext().prec = 500