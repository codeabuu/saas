from django.db import models

# Create your models here.
class PageVisit(models.Model):
    path = models.TextField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
 