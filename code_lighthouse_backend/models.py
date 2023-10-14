from django.db import models

# Create your models here.

class Challenge(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=4000)