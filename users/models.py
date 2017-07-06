from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from constants import langs

def validate_lang(value):
    if value not in langs:
        raise ValidationError('%s No such Language ' % value)

class Coder(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    institution = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    resume = models.FileField(null=True,blank=True)
    lang = models.CharField(max_length=10, default='cpp', validators=[validate_lang])

    def __unicode__(self):
        return u"%s" % self.user
