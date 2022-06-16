# Generated by Django 4.0.3 on 2022-06-16 03:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_user_follower_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follower_to',
        ),
        migrations.AddField(
            model_name='user',
            name='follow_to',
            field=models.ManyToManyField(blank=True, related_name='follow_who', to=settings.AUTH_USER_MODEL),
        ),
    ]