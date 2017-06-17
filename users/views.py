from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .modelForms import CoderForm,UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic.edit import UpdateView
from .models import Coder
from django.urls import reverse


class UserFormView(View):
    form_class1 = UserForm
    form_class2 = CoderForm
    template_name = 'users/reg_form.html'

    def get(self, request):
        form1 = self.form_class1(None)
        form2 = self.form_class2(None)
        return render(request, self.template_name,
                      {'form1' : form1,'form2':form2})

    def post(self, request):
        form1=self.form_class1(request.POST)
        form2 = self.form_class2(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            coder = form2.save(commit=False)
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password']
            email = form1.clean_email()
            user.set_password(password)
            user.save()
            coder.user = user
            coder.save()

            user = authenticate(username = username,password = password)
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('/')
        return render(request, self.template_name, {'form1': form1, 'form2': form2})


class MainPageView(View):
    template_name = 'main_page.html'

    def get(self, request):
        user = None
        if request.user.is_authenticated():
            user = request.user
        return render(request, self.template_name, {'user': user})


class LoginPageView(View):

    template_name = 'users/login_page.html'

    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect('/')

        return render(request,self.template_name)


class LogoutPageView(View):

    template_name = 'main_page.html'

    def post(self, request):
        logout(request)
        return redirect('/')


class DetailPageView(View):

    template_name = 'users/detail.html'

    def get(self,request,user):
        userobj = get_object_or_404(User,username=user)
        return render(request,self.template_name,{'user': userobj})


# edit profile fields other than user id and password


class UserUpdate(UpdateView):
    model = Coder
    fields = ['institution','city','state','resume']

    def get_object(self,*args,**kwargs):
        user = self.request.user
        return user.coder

    def get_success_url(self, *args, **kwargs):
        return reverse("home")



