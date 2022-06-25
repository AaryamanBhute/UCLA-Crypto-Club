from pyexpat import model
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    email = models.CharField(max_length=255)
    anonymous = models.BooleanField()
    assets = models.TextField()

class Post(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField()
    content = models.TextField()
    imageurl = models.TextField()