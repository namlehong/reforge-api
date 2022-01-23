from django.core.management.base import BaseCommand
import json

from reforge.apps.poe.models import TradingHallService


def gen_item(item):
    return TradingHallService(
        title=item['shortName'],
        tags=[item['category'], *item['keywords']],
        category_id=3
    )


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        with open('harvest-mods.json', 'r') as f:
            data = json.load(f)

        data.sort(key=lambda i: i['category'])

        items = list(map(gen_item, data))

        TradingHallService.objects.bulk_create(items)
