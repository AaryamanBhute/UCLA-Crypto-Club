from pyexpat import model
from django.db import models
from datetime import datetime

class UserInfoManager(models.Manager):
    def create_user_info(self, e, c=0, a="", anon=False):
        new = self.create(email=e, assets=a, cash=c, anonymous=anon)
        return new

# Create your models here.
class UserInfo(models.Model):
    email = models.CharField(max_length=255)
    anonymous = models.BooleanField()
    assets = models.TextField()
    cash = models.IntegerField()
    objects = UserInfoManager()