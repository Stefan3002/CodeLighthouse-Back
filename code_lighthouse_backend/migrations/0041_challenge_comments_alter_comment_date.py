# Generated by Django 4.2.6 on 2023-10-28 15:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0040_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='comments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='featured_in', to='code_lighthouse_backend.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 10, 28, 18, 22, 34, 96208)),
        ),
    ]
