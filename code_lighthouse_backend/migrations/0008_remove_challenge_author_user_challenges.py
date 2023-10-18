# Generated by Django 4.2.6 on 2023-10-18 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('code_lighthouse_backend', '0007_alter_challenge_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='author',
        ),
        migrations.AddField(
            model_name='user',
            name='challenges',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Author', to=settings.AUTH_USER_MODEL),
        ),
    ]
