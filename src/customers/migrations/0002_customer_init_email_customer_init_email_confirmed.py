# Generated by Django 5.1.2 on 2024-11-05 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='init_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='init_email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
