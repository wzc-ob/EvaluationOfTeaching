# Generated by Django 2.1.5 on 2019-05-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0016_remove_subject_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='age',
            field=models.CharField(default=30, max_length=3),
        ),
    ]