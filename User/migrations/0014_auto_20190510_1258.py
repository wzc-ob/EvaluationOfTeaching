# Generated by Django 2.1.5 on 2019-05-10 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0013_auto_20190509_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='e_state',
            name='student',
        ),
        migrations.RemoveField(
            model_name='e_state',
            name='teacher',
        ),
        migrations.AlterField(
            model_name='student',
            name='img',
            field=models.ImageField(blank=True, default='nopic.jpg', upload_to='files'),
        ),
        migrations.DeleteModel(
            name='E_State',
        ),
    ]