from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings

User = settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS = True
SUBSCRIPTION_PERMISSIONS = [
            ("advanced", "Advanced Perm"),  #accesed as subscriptions.advanced
            ("pro", "Pro Perm"),  #subscriptions.pro
            ("basic", "Basic Perm")  #subscriptions.Basic
        ]

class Subscription(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={
        "content_type__app_label": "subscriptions",
        "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS],
    })

    def __str__(self):
        return f"{self.name}"

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


def user_sub_post_save(sender, instance, *args, **kwargs):
    user = instance.user
    subscription_obj = instance.subscription
    groups_ids = []

    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)

    if not ALLOW_CUSTOM_GROUPS:
        # Directly set user's groups to match subscription groups
        user.groups.set(groups_ids)
    else:
        # Collect all groups linked to active subscriptions excluding the current one
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = set(subs_qs.values_list("groups__id", flat=True))

        # Calculate final groups set
        current_groups = set(user.groups.all().values_list("id", flat=True))
        final_groups_ids = list((set(groups_ids) | current_groups) - subs_groups)

        # Update the user's groups with the final list
        user.groups.set(final_groups_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)