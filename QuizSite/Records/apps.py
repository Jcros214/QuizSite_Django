from django.apps import AppConfig


class RecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Records'

class SiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Site'

