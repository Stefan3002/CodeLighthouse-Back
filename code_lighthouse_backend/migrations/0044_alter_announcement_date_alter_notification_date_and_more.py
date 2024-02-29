# Generated by Django 4.2.6 on 2024-02-29 17:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0043_contest_challenges_alter_announcement_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 2, 29, 19, 58, 37, 156380)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 29, 19, 58, 37, 153858)),
        ),
        migrations.RemoveField(
            model_name='reports',
            name='challenge',
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 2, 29, 19, 58, 37, 157397)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2024, 2, 29, 19, 58, 37, 157397)),
        ),
        migrations.AddField(
            model_name='reports',
            name='challenge',
            field=models.ManyToManyField(null=True, related_name='reports_featured_in', to='code_lighthouse_backend.challenge'),
        ),
    ]
