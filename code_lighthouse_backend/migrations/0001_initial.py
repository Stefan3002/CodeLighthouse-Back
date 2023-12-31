# Generated by Django 4.2.6 on 2023-11-14 15:24

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('provider', models.BooleanField(default=False)),
                ('password', models.CharField(blank=True, default='', max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('photoURL', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('score', models.IntegerField(default=0, max_length=10)),
                ('user_id', models.UUIDField(default=uuid.uuid4)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=4000)),
                ('slug', models.SlugField(default='')),
                ('difficulty', models.IntegerField(default=-5)),
                ('status', models.CharField(default='Reviewing', max_length=30)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='authored_challenges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2023, 11, 14, 17, 24, 1, 484665))),
                ('time', models.TimeField(default=datetime.datetime(2023, 11, 14, 17, 24, 1, 484665))),
                ('code', models.TextField(blank=True, max_length=4000)),
                ('language', models.CharField(default='Python', max_length=50)),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_submissions', to='code_lighthouse_backend.challenge')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='likes_received', to='code_lighthouse_backend.challenge')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='liked_challenges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lighthouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('enrollment_code', models.UUIDField(default=uuid.uuid4)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='authored_lighthouses', to=settings.AUTH_USER_MODEL)),
                ('people', models.ManyToManyField(related_name='enrolled_Lighthouses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('challenge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='code_lighthouse_backend.challenge')),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50)),
                ('solution', models.TextField(default='def true_function():', max_length=4000)),
                ('random_tests', models.TextField(default='def random_function():', max_length=4000)),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='codes', to='code_lighthouse_backend.challenge')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('due_time', models.TimeField()),
                ('finished', models.BooleanField(default=False)),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='featured_in', to='code_lighthouse_backend.challenge')),
                ('lighthouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='featured_in', to='code_lighthouse_backend.lighthouse')),
                ('users', models.ManyToManyField(related_name='assignments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='appuser',
            name='solved_challenges',
            field=models.ManyToManyField(blank=True, null=True, to='code_lighthouse_backend.challenge'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
