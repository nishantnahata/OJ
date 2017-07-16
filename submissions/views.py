from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from .modelForms import EditorForm, LangSelect
from django.core.files.base import ContentFile
from .models import Submission
from constants import status

lang = str(None)


@method_decorator(login_required(login_url='/'), name='dispatch')
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
            test = request.POST['inp']
            print('INP :'+test)
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
            result = submission.run(test)
            result.status = status[result.status]
            result.toe = '{:.2f}'.format(result.toe)
            submission.code.delete(save=False)
            form2 = self.form_class2(None)
            return render(request, self.template_name,
                          {'form1': form1, 'form2': form2, 'lang': lang,
                           'result': result})


"""
#include<iostream>

using namespace std;

int main()
{
    cout<<1<<endl;
    return 0;
}
"""

"""
import subprocess, os

pid = os.getpid()
print(os.getgid())
r = subprocess.Popen("ps -o cgroup "+str(pid), shell=True)

print(r.communicate()[0])
"""


class SubmissionView(View):
    template_name = 'submissions/submission_page.html'
    form_class = EditorForm

    def get(self, request, sid):
        submission = get_object_or_404(Submission, pk=sid)
        with open(submission.code.path, 'r') as f:
            code = f.read().replace('\n\r', '')
        form = self.form_class(code=code, disable=True,
                               lang=submission.lang, theme='twilight')
        return render(request, self.template_name, {'form': form})
