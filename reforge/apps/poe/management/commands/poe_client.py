from django.core.management.base import BaseCommand
from reforge.apps.poe.client import *
from reforge.apps.profiles.models import *


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('sid', nargs='+')
        pass

    def handle(self, *args, **options):
        # client = create_client(options['sid'][0])
        # info = get_account_info(client)
        info = public_profile(options['sid'][0])
        profile = Profile.objects.get(user__username='demo')
        for k, v in info.items():
            setattr(profile, k, v)
        # print(info)
        profile.save()
