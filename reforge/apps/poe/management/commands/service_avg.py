from django.core.management.base import BaseCommand

from reforge.apps.poe.tasks import service_avg_price


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        service_avg_price()
