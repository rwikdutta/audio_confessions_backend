# Generated by Django 2.0.4 on 2018-04-16 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0002_likes_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='liked',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='unliked',
        ),
    ]
