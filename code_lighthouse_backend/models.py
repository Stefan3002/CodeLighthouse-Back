from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class AppUser:
    pass


class AppUser(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(default='')

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
