from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserVouch, UserService
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


@receiver(post_save, sender=UserService)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `User` instance is created. If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    if instance:
        if instance.is_active:
            async_to_sync(channel_layer.group_send)("poe_service__%s" % instance.service_id, {
                "type": "service.update",
                "id": instance.pk,
                "service_id": instance.service_id
            })


def recount_vouch(instance):
    vouch_receiver = instance.service.user
    positive_count = UserVouch.objects.filter(service__user=vouch_receiver, karma=1).count()
    positive_unique = UserVouch.objects.filter(service__user=vouch_receiver, karma=1).order_by('user_id').distinct('user_id').count()
    negative_count = UserVouch.objects.filter(service__user=vouch_receiver, karma=-1).count()
    negative_unique = UserVouch.objects.filter(service__user=vouch_receiver, karma=-1).order_by('user_id').distinct('user_id').count()

    vouch_receiver.karma = positive_count - negative_count
    vouch_receiver.positive_karma = positive_count
    vouch_receiver.negative_karma = negative_count
    vouch_receiver.unique_positive = positive_unique
    vouch_receiver.unique_negative = negative_unique
    vouch_receiver.save()
    print('post save user_vouch_karma_count', vouch_receiver)

    async_to_sync(channel_layer.group_send)("profile__%s" % vouch_receiver.id, {
        'type': "vouch.update",
        'profile': {
            'karma': vouch_receiver.karma,
            'positive_karma': vouch_receiver.positive_karma,
            'negative_karma': vouch_receiver.negative_karma,
            'unique_positive': vouch_receiver.unique_positive,
            'unique_negative': vouch_receiver.unique_negative
        }
    })


@receiver(post_save, sender=UserVouch)
def user_vouch_karma_count(sender, instance, created, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `User` instance is created. If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    if instance:
        recount_vouch(instance)


@receiver(post_delete, sender=UserVouch)
def user_vouch_karma_count_on_delete(sender, instance, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `User` instance is created. If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    if instance:
        recount_vouch(instance)
