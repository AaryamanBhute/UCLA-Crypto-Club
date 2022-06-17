from pyexpat import model
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    email = models.CharField(max_length=255)
    anonymous = models.BooleanField()
    assets = models.TextField()