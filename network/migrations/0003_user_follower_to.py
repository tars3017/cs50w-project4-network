# Generated by Django 4.0.3 on 2022-06-16 02:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follower_to',
            field=models.ManyToManyField(blank=True, related_name='follow_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
