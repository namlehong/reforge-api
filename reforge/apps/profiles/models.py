from django.db import models

from reforge.apps.core.models import TimestampedModel


class Profile(TimestampedModel):
    # As mentioned, there is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    # Each user profile will have a field where they can tell other users
    # something about themselves. This field will be empty when the user
    # creates their account, so we specify `blank=True`.
    bio = models.TextField(blank=True)

    # In addition to the `bio` field, each user may have a profile image or
    # avatar. Similar to `bio`, this field is not required. It may be blank.
    image = models.URLField(blank=True)

    # extra for poe
    session_id = models.TextField(blank=True)

    # poe related
    name = models.CharField(max_length=200, default='')
    realm = models.CharField(max_length=200, default='')
    challenge = models.CharField(max_length=200, default='')
    achievements = models.CharField(max_length=200, default='')
    joined = models.CharField(max_length=200, default='')

    poe_account = models.JSONField(default=dict, null=True)
    last_character = models.JSONField(default=dict, null=True)

    karma = models.IntegerField(default=0)
    positive_karma = models.IntegerField(default=0)
    unique_positive = models.IntegerField(default=0)
    negative_karma = models.IntegerField(default=0)
    unique_negative = models.IntegerField(default=0)

    is_opened = models.BooleanField(default=False)
    is_stream_ready = models.BooleanField(default=False)
    is_collateral_ready = models.BooleanField(default=False)
    max_collateral_amount = models.CharField(max_length=100, blank=True, null=True)

    settings = models.JSONField(default=dict, null=True)

    def __str__(self):
        return self.user.username
