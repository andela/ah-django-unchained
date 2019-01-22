# Generated by Django 2.1.4 on 2019-01-20 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20190118_0703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='is_dispayed',
            new_name='is_displayed',
        ),
        migrations.AddField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
