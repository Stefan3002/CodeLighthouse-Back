# Generated by Django 4.2.6 on 2023-12-09 14:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0017_code_hard_tests_alter_announcement_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='exec_time',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 12, 9, 16, 20, 55, 317373)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 12, 9, 16, 20, 55, 318389)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 12, 9, 16, 20, 55, 318389)),
        ),
    ]