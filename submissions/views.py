from django.shortcuts import render, redirect
from django.views import View
from .modelForms import EditorForm
import langs


class EditorView(View):
    template_name = 'submissions/code_editor.html'
    form_class = EditorForm

    def get(self, request):
        form = self.form_class(request.user.coder.lang, None)
        return render(request, self.template_name, {'form': form, 'langs': langs.langs})

    def post(self,request):
        lang = request.POST['lang']
        if lang!=None:
            form = self.form_class(lang, None)
            return render(request, self.template_name, {'form': form, 'langs': langs.langs})
        form = self.form_class(request.POST['form'])
        if not form.is_valid():
             return redirect('ide')
        # code to be added for handling code-data which is in form
        # use Submission model to add this data to database
        return render(request, self.template_name, {'form': form, 'langs': langs.langs})