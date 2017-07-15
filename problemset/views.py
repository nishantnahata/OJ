from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.views import View

from submissions.modelForms import EditorForm, LangSelect
from submissions.models import Submission
from .models import Problem
from constants import status


class ProblemSetView(View):
    template_name = 'problemset/problem_set.html'

    # TODO: Show 25 problems per page.
    def get(self, request):
        problemset = Problem.objects.all().reverse()
        fields = Problem._meta.get_fields()
        return render(request, self.template_name, {'problemset': problemset,
                                                    'fields': fields})

lang = str(None)


class ProblemView(View):
    template_name = 'problemset/problem_page.html'
    form_class1 = EditorForm
    form_class2 = LangSelect
    lang_map = {
        'c': '.c',
        'cpp': '.cpp',
        'java': '.java',
        'python': '.py'
    }

    def get(self, request, pid):
        global lang
        if lang == 'None':
            lang = request.user.coder.lang
        # print(lang)
        form1 = self.form_class1(lang, None)
        form2 = self.form_class2(None)
        problem = get_object_or_404(Problem, pk=pid)
        return render(request, self.template_name,
                      {'problem': problem,
                       'form1': form1,
                       'form2': form2, 'lang': lang})

    def post(self, request, pid):
        global lang
        problem = get_object_or_404(Problem, pk=pid)
        if 'lang_select' in request.POST:
            form2 = self.form_class2(request.POST)
            if form2.is_valid():
                lang = form2.cleaned_lang()
                form1 = self.form_class1(lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name, {'problem': problem,
                              'form1': form1, 'form2': form2, 'lang': lang})
            else:
                form1 = self.form_class1(lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name, {'problem': problem,
                              'form1': form1, 'form2': form2, 'lang': lang})
        else:
            form1 = self.form_class1(data=request.POST, lang=lang)
            if not form1.is_valid():
                form1 = self.form_class1(lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name,
                              {'form1': form1, 'form2': form2, 'lang': lang})

            content = ContentFile(request.POST['code'])
            submission = Submission(user=request.user, lang=lang, problem=problem)
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
            result = problem.test(submission)
            result.status = status[result.status]
            result.toe = '{:.2f}'.format(result.toe)
            form2 = self.form_class2(None)
            return render(request, self.template_name,
                          {'problem': problem,
                           'form1': form1,
                           'form2': form2,
                           'lang': lang,
                           'result': result})


class StatusView(View):
    template_name = 'problemset/submissions.html'

    # TODO: Show 25 submissions per page.
    def get(self, request, pid):
        problem = get_object_or_404(Problem, pk=pid)
        submissions = problem.submission_set.all()
        return render(request, self.template_name, {'submissions': submissions})
