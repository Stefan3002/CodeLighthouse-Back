# Generated by Django 4.2.6 on 2024-01-31 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0035_alter_announcement_date_alter_notification_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 31, 16, 51, 27, 794241)),
        ),
        migrations.AlterField(
            model_name='log',
            name='time_in',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='time_out',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 31, 16, 51, 27, 792178)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 31, 16, 51, 27, 795237)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2024, 1, 31, 16, 51, 27, 795237)),
        ),
    ]
