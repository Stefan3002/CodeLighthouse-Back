# Generated by Django 4.2.6 on 2023-11-24 21:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0013_announcement_challenge_alter_announcement_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='challenge',
        ),
        migrations.AddField(
            model_name='announcement',
            name='lighthouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='code_lighthouse_backend.lighthouse'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 11, 24, 23, 24, 54, 542649)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 11, 24, 23, 24, 54, 543649)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 11, 24, 23, 24, 54, 543649)),
        ),
    ]
