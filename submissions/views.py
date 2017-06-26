import os

from django.shortcuts import render, redirect
from django.views import View

from OJ.settings import MEDIA_ROOT
from .modelForms import EditorForm, LangSelect
from django.core.files.base import ContentFile
from .models import Submission, Test

lang = str(None)


class EditorView(View):

    template_name = 'submissions/code_editor.html'
    form_class1 = EditorForm
    form_class2 = LangSelect
    lang_map = {
        'c': '.c',
        'cpp': '.cpp',
        'java': '.java',
        'python': '.py'
    }

    def get(self, request):
        global lang
        if request.user.is_anonymous:
            return redirect('/')
        if lang == 'None':
            lang = request.user.coder.lang
        # print(lang)
        form1 = self.form_class1(lang, None)
        form2 = self.form_class2(None)
        return render(request, self.template_name,
                      {'form1': form1, 'form2': form2, 'lang': lang})

    def post(self, request):
        global lang
        if 'lang_select' in request.POST:
            form2 = self.form_class2(request.POST)
            if form2.is_valid():
                lang = form2.cleaned_lang()
                form1 = self.form_class1(lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name,
                              {'form1': form1, 'form2': form2, 'lang': lang})
            else:
                form1 = self.form_class1(lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name,
                              {'form1': form1, 'form2': form2, 'lang': lang})

        else:
            form1 = self.form_class1(data=request.POST, lang=lang)
            if not form1.is_valid():
                form1 = self.form_class1(lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name,
                              {'form1': form1, 'form2': form2, 'lang': lang})

            # Take the form data in a file and store it in Submission model
            # print(lang)
            content = ContentFile(request.POST['code'])
            i_content = request.POST['inp']
            submission = Submission(user=request.user, lang=lang)
            submission.code.save('x' + self.lang_map[lang],
                                 content, save=False)
            r = submission.compile()

            # Compilation error
            if r != 200:
                submission.code.delete(save=False)
                form2 = self.form_class2(None)
                return render(request, self.template_name,
                              {'form1': form1, 'form2': form2, 'lang': lang,
                               'errors': r})
            submission.save()
            test = open(MEDIA_ROOT + '/test/x_tmp.txt', "w+")
            test.write(i_content)
            result = submission.run(test)
            os.remove(MEDIA_ROOT + '/test/x_tmp.txt')
            return redirect('/')


"""
#include<iostream>

using namespace std;

int main()
{
    cout<<1<<endl;
    return 0;
}
"""