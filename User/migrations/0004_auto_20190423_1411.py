# Generated by Django 2.1.5 on 2019-04-23 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20190423_1408'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='evaluation',
            table='e_evaluation',
        ),
        migrations.AlterModelTable(
            name='subject',
            table='e_subject',
        ),
    ]
