from django.apps import AppConfig


class EproxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eProx'
    # def ready(self):
    #     import eProx.signals
