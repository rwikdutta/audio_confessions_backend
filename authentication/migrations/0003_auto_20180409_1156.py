# Generated by Django 2.0.4 on 2018-04-09 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20180409_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmodel',
            name='passout_year',
            field=models.DecimalField(choices=[(2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], decimal_places=0, max_digits=4),
        ),
    ]
