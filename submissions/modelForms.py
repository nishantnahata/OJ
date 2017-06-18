from django import forms
from django_ace import AceWidget

mode_map={
    'c':'c_cpp',
    'cpp':'c_cpp',
    'java':'java',
    'python':'python',
}

class EditorForm(forms.Form):
    code = forms.CharField()

    def __init__(self, lang='cpp', *args, **kwargs):
        super(EditorForm,self).__init__(*args, **kwargs)
        self.fields['code'] = forms.CharField(widget=AceWidget(mode=mode_map[lang],
                                                               theme='daylight'))

