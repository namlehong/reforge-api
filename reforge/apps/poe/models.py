import re

from autoslug import AutoSlugField
from django.db import models

from reforge.apps.core.models import TimestampedModel


class League(TimestampedModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = None

    def __str__(self):
        return self.name


class Currency(TimestampedModel):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    chaos_equivalent = models.FloatField(default=0)

    class Meta:
        ordering = None

    def __str__(self):
        return 'Currency: %s' % self.name


class TradingHallCategory(TimestampedModel):
    title = models.CharField(db_index=True, max_length=255)
    slug = AutoSlugField(db_index=True, populate_from='title')
    is_active = models.BooleanField(db_index=True, default=True)

    class Meta:
        ordering = None

    def __str__(self):
        return self.title


class TradingHallService(TimestampedModel):
    title = models.CharField(db_index=True, max_length=1000)
    slug = AutoSlugField(db_index=True, populate_from='title')
    is_active = models.BooleanField(db_index=True, default=True)
    category = models.ForeignKey(TradingHallCategory, on_delete=models.CASCADE)
    tags = models.JSONField(default=list)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return self.title


class TradingHallPrice(TimestampedModel):
    service = models.ForeignKey(TradingHallService, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    average = models.FloatField(default=0)
    median = models.FloatField(default=0)

    class Meta:
        ordering = None
        unique_together = [('service', 'league')]


class UserService(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    service = models.ForeignKey(TradingHallService, on_delete=models.CASCADE)
    item_level = models.IntegerField(default=0, db_index=True)
    price = models.CharField(db_index=True, max_length=200)
    float_price = models.FloatField(db_index=True, default=0)
    user_credit = models.IntegerField(db_index=True, default=0)
    chaos_equivalent = models.FloatField(default=0)
    ex_equivalent = models.FloatField(default=0)
    tags = models.JSONField(default=list)
    options = models.JSONField(default=dict)
    is_active = models.BooleanField(db_index=True, default=True)
    is_delete = models.BooleanField(db_index=True, default=False)

    class Meta:
        unique_together = [('user', 'league', 'service')]
        ordering = ('chaos_equivalent',)

    @staticmethod
    def get_float_price(price):
        pattern = '\d+\.?\d*'
        matched = re.findall(pattern, price)

        if matched:
            return float(matched[0])
        else:
            return 0


class UserVouch(TimestampedModel):
    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    service = models.ForeignKey(UserService, on_delete=models.CASCADE)
    karma = models.IntegerField(default=0, db_index=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = [('user', 'service')]
        ordering = ('-updated_at',)
