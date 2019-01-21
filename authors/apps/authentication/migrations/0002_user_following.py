# Generated by Django 2.1.4 on 2019-01-16 17:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='friends.Friend', to=settings.AUTH_USER_MODEL),
        ),
    ]
