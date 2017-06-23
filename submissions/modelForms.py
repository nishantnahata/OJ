from django import forms
from django.core.exceptions import ValidationError
from django_ace import AceWidget

mode_map={
    'c': 'c_cpp',
    'cpp': 'c_cpp',
    'java': 'java',
    'python': 'python',
    '': 'c_cpp',
}

LANG_CHOICES = (
    ('-', '-'),
    ('cpp', 'cpp'),
    ('c', 'c'),
    ('java', 'java'),
    ('python', 'python'),
)


class EditorForm(forms.Form):
    code = forms.CharField()

    def __init__(self, lang='cpp', *args, **kwargs):
        super(EditorForm,self).__init__(*args, **kwargs)
        self.fields['code'] = forms.CharField(widget=AceWidget(mode=mode_map[lang],
                                                               theme='daylight'))



class LangSelect(forms.Form):
    lang = forms.ChoiceField(choices=LANG_CHOICES)

    def cleaned_lang(self):
        lang = self.cleaned_data['lang']
        lang = dict(self.fields['lang'].choices)[lang]
        if lang == '-':
            raise ValidationError(u'Language cannot be left blank')
        return lang
