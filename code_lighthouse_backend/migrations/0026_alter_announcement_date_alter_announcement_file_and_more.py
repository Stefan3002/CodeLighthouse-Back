# Generated by Django 4.2.6 on 2024-01-21 19:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0025_announcement_file_alter_announcement_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 21, 21, 9, 14, 370660)),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='file',
            field=models.FileField(default=None, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 21, 21, 9, 14, 369645)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 21, 21, 9, 14, 372919)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2024, 1, 21, 21, 9, 14, 372919)),
        ),
    ]
