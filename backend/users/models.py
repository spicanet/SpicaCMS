# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField('Bio', blank=True, null=True)
    social_links = models.JSONField('Social Links', blank=True, null=True)