from django.apps import AppConfig


class PoeConfig(AppConfig):
    name = 'reforge.apps.poe'

    def ready(self):
        import reforge.apps.poe.receivers
