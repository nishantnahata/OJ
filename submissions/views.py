from django.shortcuts import render, redirect
from django.views import View
from .modelForms import EditorForm, LangSelect


class EditorView(View):
    template_name = 'submissions/code_editor.html'
    form_class1 = EditorForm
    form_class2 = LangSelect
    lang = str(None)

    def get(self, request):
        if self.lang == 'None':
            self.lang = request.user.coder.lang
        print(self.lang)
        form1 = self.form_class1(self.lang, None)
        form2 = self.form_class2(None)
        return render(request, self.template_name,
                      {'form1': form1, 'form2': form2, 'lang': self.lang})

    def post(self, request):

        if 'lang_select' in request.POST:
            form2 = self.form_class2(request.POST)
            if form2.is_valid():
                self.lang = form2.cleaned_lang()
                form1 = self.form_class1(self.lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name,
                              {'form1': form1, 'form2': form2, 'lang': self.lang})
            else:
                form1 = self.form_class1(self.lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name,
                              {'form1': form1, 'form2': form2, 'lang': self.lang})

        else:
            form1 = self.form_class1(data=request.POST)
            if not form1.is_valid():
                form1 = self.form_class1(self.lang, None)
                form2 = self.form_class2(None)
                return render(request, self.template_name,
                              {'form1': form1, 'form2': form2, 'lang': self.lang})

            #Take the form data in a file and store it in Submission model
            return redirect('/')
