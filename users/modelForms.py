from django.contrib.auth.models import User
from django import forms
from .models import Coder
LANG_CHOICES = (
    ('-', '-'),
    ('cpp', 'cpp'),
    ('c', 'c'),
    ('java', 'java'),
    ('python', 'python'),
)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class CoderForm(forms.ModelForm):
    lang = forms.ChoiceField(choices=LANG_CHOICES)

    class Meta:
        model = Coder
        fields = ['institution','city','state','resume','lang']
