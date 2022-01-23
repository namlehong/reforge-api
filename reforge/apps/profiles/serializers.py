from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    poe = serializers.JSONField(source='last_character')

    # settings = serializers.JSONField()

    class Meta:
        model = Profile
        fields = (
            'id', 'username', 'poe', 'karma', 'positive_karma',
            'name', 'realm', 'challenge', 'achievements', 'joined',
            'negative_karma', 'user', 'unique_positive', 'unique_negative',
            'is_stream_ready', 'is_collateral_ready', 'max_collateral_amount', 'last_character'
        )
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
