# Generated by Django 2.0.4 on 2018-04-26 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confessions', '0006_confessions_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='confessions',
            name='comments_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='confessions',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
    ]
