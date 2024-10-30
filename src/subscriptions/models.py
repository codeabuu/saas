from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        permissions = [
            ("advanced", "Advanced Perm"),  #accesed as subscriptions.advanced
            ("pro", "Pro Perm"),  #subscriptions.pro
            ("basic", "Basic Perm")  #subscriptions.Basic
        ]
