from rest_framework import serializers

from reforge.apps.poe.models import League, TradingHallCategory, TradingHallService, TradingHallPrice, \
    UserService, Currency, UserVouch
from reforge.apps.profiles.serializers import ProfileSerializer


class BenchCraftSerializer(serializers.Serializer):
    mod = serializers.CharField()
    is_remove = serializers.BooleanField(default=False)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'chaos_equivalent', 'league']


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'name', 'code']


class TradingHallCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingHallCategory
        fields = ['id', 'title', 'slug']


class TradingHallServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingHallService
        fields = ['id', 'title', 'slug', 'category', 'tags', 'is_active']


class TradingHallPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingHallPrice
        fields = ['id', 'service', 'league', 'average', 'median']


class UserServiceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    # username = serializers.JSONField(source='user.username', read_only=True)
    # profile = serializers.JSONField(source='user.profile.poe_account', read_only=True)
    profile = ProfileSerializer(source='user', many=False, read_only=True)

    # approved = serializers.IntegerField(source='user.profile.positive_karma', read_only=True)
    # disapproved = serializers.IntegerField(source='user.profile.negative_karma', read_only=True)

    class Meta:
        model = UserService
        fields = [
            'id', 'service', 'league', 'user', 'price', 'chaos_equivalent', 'profile',
            'is_active', 'item_level', 'float_price', 'updated_at'
        ]

        read_only_fields = ['updated_at']

    def save(self, **kwargs):
        price = self.validated_data.get('price')

        if not price:
            return super(UserServiceSerializer, self).save(**kwargs)

        league_id = self.validated_data.get('league')
        service_id = self.validated_data.get('service')
        float_price = UserService.get_float_price(price)

        if float_price:
            if 'ex' in price.lower():
                cur, _ = Currency.objects.get_or_create(name='Exalted Orb', league=league_id,
                                                        defaults=dict(chaos_equivalent=80))
                chaos_equivalent = float_price * cur.chaos_equivalent
            else:
                chaos_equivalent = float_price
        else:
            service_price, _ = TradingHallPrice.objects.get_or_create(service=service_id, league=league_id)
            chaos_equivalent = service_price.median

        super().save(
            float_price=float_price,
            chaos_equivalent=chaos_equivalent,
            **kwargs
        )


class UserVouchSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    sender_username = serializers.CharField(source='user.name', read_only=True)
    sender = ProfileSerializer(source='user', many=False, read_only=True)
    receiver_username = serializers.CharField(source='service.user.name', read_only=True)
    receiver = ProfileSerializer(source='service.user', many=False, read_only=True)
    service_title = serializers.CharField(source='service.service.title', read_only=True)

    class Meta:
        model = UserVouch
        fields = [
            'id', 'service',
            'user', 'karma', 'sender', 'receiver',
            'note', 'updated_at', 'sender_username', 'service_title', 'receiver_username'
        ]

    def create(self, validated_data):
        instance, created = UserVouch.objects.get_or_create(
            user=validated_data['user'],
            service=validated_data['service'],
            defaults={
                'karma': validated_data.get('karma'),
                'note': validated_data.get('note', '')
            }
        )

        if not created:
            instance.karma = validated_data['karma']
            instance.note = validated_data.get('note', '')
            instance.save()

        return instance
