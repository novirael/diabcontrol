from django.apps import AppConfig


class RestApiConfig(AppConfig):
    name = 'rest_api'

    def ready(self):
        from rest_api import signals
