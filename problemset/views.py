from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Problem
# Create your views here.


class ProblemSetView(View):
    template_name = 'problemset/problem_set.html'

    # TODO: Show 25 problems per page.
    def get(self, request):
        problemset = Problem.objects.all()
        fields = Problem._meta.get_fields()
        return render(request, self.template_name, {'problemset': problemset,
                                                    'fields': fields})


class ProblemView(View):
    template_name = 'problemset/problem_page.html'

    def get(self, request, pid):
        problem = get_object_or_404(Problem, pk=pid)
        return render(request, self.template_name, {'problem': problem})


class StatusView(View):
    template_name = 'problemset/submissions.html'

    # TODO: Show 25 submissions per page.
    def get(self, request, pid):
        problem = get_object_or_404(Problem, pk=pid)
        submissions = problem.submission_set.all()
        return render(request, self.template_name, {'submissions': submissions})
