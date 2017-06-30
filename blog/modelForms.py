from django import forms

class BlogForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
