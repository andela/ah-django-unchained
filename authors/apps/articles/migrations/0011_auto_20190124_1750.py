# Generated by Django 2.1.5 on 2019-01-24 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20190123_0836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='dislikes',
            new_name='user_id_dislikes',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='likes',
            new_name='user_id_likes',
        ),
    ]
