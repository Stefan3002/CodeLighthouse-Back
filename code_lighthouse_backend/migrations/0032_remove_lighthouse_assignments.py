# Generated by Django 4.2.6 on 2023-10-24 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0031_assignment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lighthouse',
            name='assignments',
        ),
    ]