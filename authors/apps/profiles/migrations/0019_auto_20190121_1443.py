# Generated by Django 2.1.4 on 2019-01-21 14:43

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0018_auto_20190121_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='', max_length=255, verbose_name='image'),
        ),
    ]
