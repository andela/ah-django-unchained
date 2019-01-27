# Generated by Django 2.1.5 on 2019-01-28 09:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_merge_20190128_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='user_id_dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL),
        ),
    ]