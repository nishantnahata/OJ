from django.conf.urls import url
from users import views

app_name = 'users'

urlpatterns = [

    # profile url
    url(r'^(?P<user>[.\-_\w]+)/', views.DetailPageView.as_view(), name='detail'),
]