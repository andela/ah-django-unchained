# Generated by Django 2.1.5 on 2019-02-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0032_auto_20190223_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='ratings',
        ),
        migrations.AddField(
            model_name='article',
            name='average_rating',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]