from django.core.management.base import BaseCommand

from reforge.apps.poe import auth


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+', type=str)

    def handle(self, *args, **options):
        username = auth.username(options['id'])

        print(username)