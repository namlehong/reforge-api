from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    last_character = serializers.SerializerMethodField()
    # poe = serializers.JSONField(source='last_character')

    # settings = serializers.JSONField()

    class Meta:
        model = Profile
        fields = (
            'id', 'username', 'karma', 'positive_karma',
            'name', 'realm', 'challenge', 'achievements', 'joined',
            'negative_karma', 'user', 'unique_positive', 'unique_negative',
            'is_stream_ready', 'is_collateral_ready', 'max_collateral_amount', 'last_character', 'characters'
        )
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'

    def get_username(self, obj):
        return obj.poe_account.get('name')

    def get_last_character(self, obj):
        return obj.characters[0]
