from django.core.management.base import BaseCommand
from reforge.apps.poe.models import UserVouch
from django.db.models import Count

class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        positive = UserVouch.objects.filter(karma=1).values('service__user_id').order_by('service__user_id').annotate(total=Count('service__user_id'))
        print(positive)
