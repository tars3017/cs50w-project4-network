# Generated by Django 4.0.3 on 2022-06-29 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_remove_user_follow_to_remove_user_followers_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='like_post',
            field=models.ManyToManyField(blank=True, related_name='follow_who', to='network.post'),
        ),
    ]
