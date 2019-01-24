# Generated by Django 2.1.4 on 2019-01-23 15:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_auto_20190123_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='favorite',
            field=models.ManyToManyField(default=False, related_name='favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]
