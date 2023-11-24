# Generated by Django 4.2.6 on 2023-11-24 13:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0008_lighthouse_archived_alter_submission_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 11, 24, 15, 29, 0, 184168)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2023, 11, 24, 15, 29, 0, 184168)),
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=30)),
                ('comment', models.TextField(max_length=1000)),
                ('closed', models.BooleanField(default=False)),
                ('assigned_admin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reports_admined', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
