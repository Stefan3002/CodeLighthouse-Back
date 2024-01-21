# Generated by Django 4.2.6 on 2024-01-21 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0029_alter_announcement_date_alter_announcement_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 21, 21, 17, 55, 313291)),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='file',
            field=models.FileField(default='uploads/files', upload_to='uploads/files'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 21, 21, 17, 55, 312292)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 21, 21, 17, 55, 314295)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2024, 1, 21, 21, 17, 55, 314295)),
        ),
    ]
