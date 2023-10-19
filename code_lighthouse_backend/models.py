import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class AppUser:
    pass


class AppUser(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(default='')
    user_id = models.UUIDField(default=uuid.uuid4, editable=True)

    def __str__(self):
        return self.username

    def natural_key(self):
        return self.username, self.email, self.id


class Challenge(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=4000)
    slug = models.SlugField(default='')
    difficulty = models.IntegerField(default=-5)
    author = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name='Challenges', null=True, blank=True)

    def __str__(self):
        return self.title


class Lighthouse(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    enrollment_code = models.UUIDField(default=uuid.uuid4, editable=True)
    author = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING, related_name='Lighthouses', null=True, blank=True)
    people = models.ManyToManyField(AppUser, related_name='Enrolled_Lighthouses')


    def __str__(self):
        return f'{self.name} by {self.author.username}'