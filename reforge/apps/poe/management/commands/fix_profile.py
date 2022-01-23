from django.core.management.base import BaseCommand

from reforge.apps.poe.client import public_profile
from reforge.apps.profiles.models import *


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        for p in Profile.objects.all():
            info = public_profile(p.user.username)
            print(info)
            if info.get('name'):
                for k, v in info.items():
                    setattr(p, k, v)
                    p.save()
