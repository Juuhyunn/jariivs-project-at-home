# Generated by Django 3.2.5 on 2021-12-12 17:19

import datetime
from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0005_auto_20211209_2357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='event_repeat',
        ),
        migrations.AddField(
            model_name='routine',
            name='days',
            field=django_mysql.models.ListTextField(models.CharField(max_length=255), null=True, size=None),
        ),
        migrations.AddField(
            model_name='routine',
            name='hours',
            field=django_mysql.models.ListTextField(models.CharField(max_length=255), null=True, size=None),
        ),
        migrations.AddField(
            model_name='routine',
            name='location',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='routine',
            name='contents',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='routine',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 13, 2, 19, 11, 868153)),
        ),
        migrations.AlterField(
            model_name='routine',
            name='cron',
            field=django_mysql.models.ListTextField(models.CharField(max_length=255), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='routine',
            name='log_id',
            field=django_mysql.models.ListTextField(models.IntegerField(), null=True, size=None),
        ),
    ]