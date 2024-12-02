from django.db import models
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
import helpers.billing
from django.urls import reverse
from django.db.models import Q

User = settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS = True
SUBSCRIPTION_PERMISSIONS = [
            ("advanced", "Advanced Perm"),  #accesed as subscriptions.advanced
            ("pro", "Pro Perm"),  #subscriptions.pro
            ("basic", "Basic Perm")  #subscriptions.Basic
        ]

class Subscription(models.Model):
    """stripe product"""
    name = models.CharField(max_length=120)
    subtitle = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={
        "content_type__app_label": "subscriptions",
        "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS],
    })
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    order = models.IntegerField(default=-1, help_text='order on django pricing page')
    featured = models.BooleanField(default=True, help_text='Featured on django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(help_text="Features for pricing, separated by new line", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["order", "featured", "-updated"]
        permissions = SUBSCRIPTION_PERMISSIONS

    def get_features_as_list(self):
        if not self.features:
            return []
        return [x.strip() for x in self.features.split("\n")]
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None   # Check if the instance is new
        super().save(*args, **kwargs)  #Save the instance to generate an ID

        if is_new and not self.stripe_id:
            stripe_id = helpers.billing.create_product(
                name=self.name,
                metadata={"subscription_plan_id": self.id},
                raw=False
            )
            self.stripe_id = stripe_id
            super().save(update_fields=["stripe_id"])

class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        TRIALING = 'trialing', 'Trialing'
        INCOMPLETE = 'incomplete', 'Incomplete'
        INCOMPLETE_EXPIRED = 'incomplete_expired', 'Incomplete Expired'
        PAST_DUE = 'past_due', 'Past Due'
        CANCELED = 'canceled', 'Canceled'
        UNPAID = 'unpaid', 'Unpaid'
        PAUSED = 'paused', 'Paused'

class UserSubscriptionQuerySet(models.QuerySet):
    def by_active_trialing(self):
        active_qs_lookup = (
            Q(status=SubscriptionStatus.ACTIVE) |
            Q(status=SubscriptionStatus.TRIALING)
        )
        return self.filter(active_qs_lookup)
    
    def by_user_ids(self, user_ids=None):
        qs=self
        if isinstance(user_ids, list):
            qs=self.filter(user_id__in=user_ids)
        elif isinstance(user_ids, int):
            qs=self.filter(user_id__in=[user_ids])
        return qs

#custom models manager
class UserSubscriptionManager(models.Manager):
    def get_queryset(self):
        return UserSubscriptionQuerySet(self.model, using=self._db)
    
    # def by_user_ids(self, user_ids=None):
    #     return self.get_queryset().by_user_ids(user_ids=user_ids)

        
class UserSubscription(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=True)
    user_cancelled = models.BooleanField(default=False)
    original_period_start = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    current_period_start = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    current_period_end = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    cancel_at_period_end = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, null=True, blank=True)

    objects = UserSubscriptionManager()


    def get_absolute_url(self):
        return reverse("user_subscription")
    
    def get_cancel_url(self):
        return reverse("user_subscription_cancel")

    @property
    def is_active_status(self):
        return self.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING, ]

    @property
    def plan_name(self):
        if not self.subscription:
            return None
        return self.subscription.name

    def serialize(self):
        return {
            "Plan_name": self.plan_name,
            "status": self.status,
            "current_period_start": self.current_period_start,
            "current_period_end":  self.current_period_end,
        }

    
    def save(self, *args, **kwargs):
        if (self.original_period_start is None and
            self.current_period_start is not None):
            self.original_period_start = self.current_period_start
        super().save(*args, **kwargs)


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


class SubscriptionPrice(models.Model):
    """sub price=stripe price"""
    class IntervalChoices(models.TextChoices):
        MONTHLY = 'month', 'Monthly'
        YEARLY = 'year', 'Yearly'
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    stripe_id = models.CharField(max_length=255, null=True, blank=True)
    interval = models.CharField(max_length=120, default=IntervalChoices.MONTHLY, choices=IntervalChoices.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=20.00)
    order = models.IntegerField(default=-1, help_text='order on django pricing page')
    featured = models.BooleanField(default=True, help_text='Featured on django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'featured', '-updated']

    def get_checkout_url(self):
        return reverse("sub-price-checkout",
                    kwargs={"price_id": self.id})
    @property
    def display_features_list(self):
        if not self.subscription:
            return []
        return self.subscription.get_features_as_list()
    
    @property
    def display_sub_name(self):
        if not self.subscription:
            return "Plan"
        return self.subscription.name
    
    @property
    def display_sub_title(self):
        if not self.subscription:
            return "Plan"
        return self.subscription.subtitle
    
    @property
    def stripe_currency(self):
        return 'USD'
    @property
    def stripe_price(self):
        """remove decs"""
        return int(self.price * 100)

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if the instance is new
        super().save(*args, **kwargs)  # Save the instance to generate an ID

        if is_new and not self.stripe_id and self.product_stripe_id is not None:
            stripe_id = helpers.billing.create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                interval=self.interval,
                product=self.product_stripe_id,
                metadata={"subscription_plan_price_id": self.id},
            )
            self.stripe_id = stripe_id
            super().save(update_fields=["stripe_id"])
        if self.featured and self.subscription:
            SubscriptionPrice.objects.filter(
                subscription=self.subscription,
                interval=self.interval
            ).exclude(id=self.id).update(featured=False)