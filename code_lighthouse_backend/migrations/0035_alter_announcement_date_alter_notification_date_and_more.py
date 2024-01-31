# Generated by Django 4.2.6 on 2024-01-31 14:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0034_announcement_file_alter_announcement_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 31, 16, 49, 41, 543761)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 31, 16, 49, 41, 542762)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 31, 16, 49, 41, 544763)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2024, 1, 31, 16, 49, 41, 544763)),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_in', models.DateTimeField()),
                ('time_out', models.DateTimeField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
