from django.apps import AppConfig


class ProfileAppConfig(AppConfig):
    name = 'reforge.apps.profiles'
    label = 'profiles'
    verbose_name = 'Profile'

    def ready(self):
        import reforge.apps.profiles.receivers


# This is how we register our custom app config with Django. Django is smart
# enough to look for the `default_app_config` property of each registered app
# and use the correct app config based on that value.
default_app_config = 'reforge.apps.profiles.ProfileAppConfig'
