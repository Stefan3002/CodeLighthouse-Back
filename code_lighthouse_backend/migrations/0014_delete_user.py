# Generated by Django 4.2.6 on 2023-10-18 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0013_remove_user_email_remove_user_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]