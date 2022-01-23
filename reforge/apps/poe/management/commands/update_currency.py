from django.core.management.base import BaseCommand
from reforge.apps.poe.tasks import update_currency


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        update_currency()
