from django.db import models
from django.contrib.auth.models import User

class Coder(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    institution = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    resume = models.FileField(null=True,blank=True)