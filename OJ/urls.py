"""OJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from users.views import MainPageView, UserFormView, LoginPageView, LogoutPageView
from submissions.views import EditorView
from django.conf import settings
from django.conf.urls.static import static
from blog.views import BlogDisplay

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #Home page url
    url(r'^$', MainPageView.as_view(),name='home'),

    # user registration url
    url(r'^register/$', UserFormView.as_view(),name='register'),

    #Login page url
    url(r'^login/$', LoginPageView.as_view(),name='login'),

    #Logout page url
    url(r'^logout/$', LogoutPageView.as_view(), name='logout'),

    # users app
    url(r'^users/',include('users.urls')),

    #submissions app
    url(r'^submissions/',include('submissions.urls')),

    #ide
    url(r'^ide/$', EditorView.as_view(), name='ide'),

    #blog
    url(r'^blog/$',BlogDisplay.as_view(),name='blog'),

    #problemset
    url(r'^problemset/',include('problemset.urls')),

    #zinnias blog
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
