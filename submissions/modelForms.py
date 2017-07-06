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
    inp = forms.CharField(widget=forms.Textarea, empty_value=True)

    def __init__(self, lang='cpp', disable=False,
                 code=None, theme='daylight', *args, **kwargs):
        super(EditorForm,self).__init__(*args, **kwargs)
        wg = AceWidget(mode=mode_map[lang],
                       theme=theme,
                       attrs={'readonly':'readonly'})
        # TODO: Make the code field uneditable.
        self.fields['code'] = forms.CharField(
            widget=wg, disabled=disable,
            initial=code,
        )


class LangSelect(forms.Form):
    lang = forms.ChoiceField(choices=LANG_CHOICES)

    def cleaned_lang(self):
        lang = self.cleaned_data['lang']
        lang = dict(self.fields['lang'].choices)[lang]
        if lang == '-':
            raise ValidationError(u'Language cannot be left blank')
        return lang
