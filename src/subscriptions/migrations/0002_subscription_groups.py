# Generated by Django 5.1.2 on 2024-10-31 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='groups',
            field=models.ManyToManyField(to='auth.group'),
        ),
    ]
