# Generated by Django 4.2.6 on 2023-10-28 15:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0039_challenge_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('date', models.DateField(default=datetime.datetime(2023, 10, 28, 18, 19, 55, 853819))),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='code_lighthouse_backend.appuser')),
            ],
        ),
    ]
