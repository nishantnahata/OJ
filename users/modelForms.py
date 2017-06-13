from django.contrib.auth.models import User
from django import forms
from .models import Coder

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=['username','first_name','last_name','email','password']

class CoderForm(forms.ModelForm):

    class Meta:
        model = Coder
        fields = ['institution','city','state','resume']

