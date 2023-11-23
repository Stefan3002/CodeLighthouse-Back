import datetime
import uuid
from time import timezone

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.

class AppUser(AbstractUser):
    provider = models.BooleanField(default=False)
    password = models.CharField(max_length=130, default='', blank=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(default='', unique=True)
    photoURL = models.CharField(max_length=200, default='', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    admin_user = models.BooleanField(default=False)
    score = models.IntegerField(max_length=10, default=0)
    user_id = models.UUIDField(default=uuid.uuid4, editable=True)
    solved_challenges = models.ManyToManyField('Challenge', null=True, blank=True)
    def __str__(self):
        return self.username

    def natural_key(self):
        return self.username, self.email, self.id


class Comment(models.Model):
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(AppUser, related_name='comments', on_delete=models.DO_NOTHING)
    # date = models.DateField(default=datetime.datetime.now)
    challenge = models.ForeignKey('Challenge', on_delete=models.DO_NOTHING, related_name='comments', blank=True, null=True)

    def __str__(self):
        return f'{self.author} on {self.challenge}'

class Challenge(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=4000)
    slug = models.SlugField(default='')
    difficulty = models.IntegerField(default=-5)
    author = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name='authored_challenges', null=True, blank=True)
    public = models.BooleanField(default=False)
    private = models.BooleanField(default=True)
    status = models.CharField(max_length=30, default='Reviewing')
    denied = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Challenge, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} by {self.author}'

class Code(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='codes',  on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=50)
    solution = models.TextField(max_length=4000, default='def true_function():')
    random_tests = models.TextField(max_length=4000, default='def random_function():')

    def __str__(self):
        return f'{self.challenge}, {self.language}'


class Lighthouse(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    enrollment_code = models.UUIDField(default=uuid.uuid4, editable=True)
    author = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name='authored_lighthouses', null=True, blank=True)
    people = models.ManyToManyField(AppUser, related_name='enrolled_Lighthouses')
    public = models.BooleanField(default=False)
    # assignments = models.ManyToManyField(Challenge, related_name='featured_in', blank=True)


    def __str__(self):
        return f'{self.name} by {self.author.username}'


class Assignment(models.Model):
    due_date = models.DateField()
    due_time = models.TimeField()
    lighthouse = models.ForeignKey(Lighthouse, related_name='featured_in', on_delete=models.DO_NOTHING, null=True)
    challenge = models.ForeignKey(Challenge, related_name='featured_in', on_delete=models.DO_NOTHING, null=True)
    users = models.ManyToManyField(AppUser, related_name='assignments')
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.lighthouse_id} - {self.challenge} - {self.due_date}'


class Like(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, related_name='liked_challenges', null=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, related_name='likes_received')


class Submission(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, related_name='submissions', null=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, related_name='challenge_submissions')
    date = models.DateField(default=datetime.datetime.now())
    time = models.TimeField(default=datetime.datetime.now())
    code = models.TextField(max_length=4000, blank=True)
    language = models.CharField(max_length=50, default='Python')

    def __str__(self):
        return f'{self.user} on {self.challenge} on {self.date} - {self.time}'
