import re
import statistics
from collections import defaultdict
from datetime import timedelta

from django.utils.timezone import now

from . import ninja
from .models import League, Currency, UserService, TradingHallPrice
from celery import shared_task


@shared_task()
def update_currency():
    for league in League.objects.filter(is_active=True):
        s = ninja.currency_overview(league.code)
        for name, chaos_equivalent in s:
            obj, created = Currency.objects.get_or_create(
                name=name,
                league=league,
                defaults=dict(chaos_equivalent=chaos_equivalent)
            )

            if not created:
                obj.chaos_equivalent = chaos_equivalent
                obj.save()


@shared_task()
def service_avg_price():
    half_hour_ago = now() - timedelta(minutes=30)
    for league in League.objects.all():
        data = defaultdict(list)

        for service_id, chaos_equivalent in UserService.objects.filter(
                league=league,
                chaos_equivalent__gt=0,
                is_active=True,
                updated_at__gte=half_hour_ago
        ).values_list('service_id', 'chaos_equivalent'):
            data[service_id].append(chaos_equivalent)

        for service_id, prices in data.items():

            _avg = sum(prices) / len(prices)
            _median = statistics.median(prices)

            print(league, service_id, _avg, _median)

            obj, created = TradingHallPrice.objects.get_or_create(
                league=league,
                service_id=service_id,
                defaults=dict(
                    average=_avg,
                    median=_median
                )
            )

            if not created:
                obj.average = _avg
                obj.median = _median
                obj.save()


@shared_task()
def fix_user_price():
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


@shared_task()
def fix_hall():
    update_currency()
    service_avg_price()
    fix_user_price()
