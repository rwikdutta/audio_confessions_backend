# Generated by Django 2.0.4 on 2018-04-16 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0003_auto_20180416_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
    ]
