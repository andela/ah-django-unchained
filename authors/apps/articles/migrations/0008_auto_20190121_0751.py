# Generated by Django 2.1.4 on 2019-01-21 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20190120_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_displayed',
        ),
        migrations.AddField(
            model_name='article',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
