# Generated by Django 4.2.6 on 2023-10-23 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('code_lighthouse_backend', '0027_appuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='authored_challenges', to='code_lighthouse_backend.appuser'),
        ),
    ]
