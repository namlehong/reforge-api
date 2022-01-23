from django.core.management.base import BaseCommand
import re
from reforge.apps.poe.models import *
from reforge.apps.poe.tasks import update_currency


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        update_currency()
        cur_exchange = dict(Currency.objects.filter(name='Exalted Orb').values_list('league', 'chaos_equivalent'))

        pattern = '\d+\.?\d*'

        for i in UserService.objects.all():

            matched = re.findall(pattern, i.price)

            if not matched:
                continue

            num_price = float(matched[0])

            if 'ex' in i.price.lower():
                i.ex_equivalent = num_price
                UserService.objects.filter(pk=i.pk).update(
                    ex_equivalent=num_price,
                    chaos_equivalent=num_price * cur_exchange.get(i.league_id, 80)
                )
            else:
                UserService.objects.filter(pk=i.pk).update(
                    ex_equivalent=0,
                    chaos_equivalent=num_price
                )
