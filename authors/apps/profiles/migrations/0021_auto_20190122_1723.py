# Generated by Django 2.1.4 on 2019-01-22 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0020_auto_20190121_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default='empty', max_length=200),
        ),
    ]
