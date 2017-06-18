from django.core.exceptions import ValidationError
from django.db import models
from langs import langs


def validate_lang(value):
    if value not in langs:
        raise ValidationError('%s No such Language ' % value)

class Submission(models.Model):
    lang = models.CharField(validators=[validate_lang], max_length=10, default='cpp')
    code = models.FileField()
    status = models.CharField(max_length=10, blank=True)