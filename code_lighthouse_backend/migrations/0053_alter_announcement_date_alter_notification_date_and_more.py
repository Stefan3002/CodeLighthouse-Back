# Generated by Django 4.2.6 on 2024-05-11 19:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0052_remove_reports_challenge_reports_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 5, 11, 22, 15, 6, 371149)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 11, 22, 15, 6, 369149)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='url',
            field=models.URLField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 5, 11, 22, 15, 6, 373149)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2024, 5, 11, 22, 15, 6, 373149)),
        ),
    ]
