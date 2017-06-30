from django.shortcuts import render,redirect
from .models import BlogEntry
from django.views import View
from .modelForms import BlogForm
# Create your views here.

class BlogDisplay(View):
    template_name = 'blog/display.html'
    form_class = BlogForm


    def get(self,request):
        form = self.form_class(None)
        if request.user.is_authenticated :
            user = request.user
            posts = user.blogentry_set.all()
        else:
            posts = BlogEntry.objects.all()
        return render(request,self.template_name,{'posts': posts,'form': form})

    def post(self,request):
        form = self.form_class(request.POST)
        blog = BlogEntry()
        user = request.user
        posts = user.blogentry_set.all()
        blog.user = user
        blog.data = request.POST['text']
        blog.save()
        return render(request,self.template_name,{'posts': posts,'form': form})

