# Generated by Django 4.2.6 on 2023-10-24 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0033_assignment_challenge_alter_assignment_lighthouse_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='users_id',
            new_name='users',
        ),
    ]
