from django.conf.urls import url
from .views import ProblemSetView, ProblemView, StatusView

app_name = 'problemset'

urlpatterns = [
    url(r'^$', ProblemSetView.as_view(), name='problemset'),
    url(r'^(?P<pid>[.\-_\w]+)/$', ProblemView.as_view(), name='problem'),
    url(r'^(?P<pid>[.\-_\w]+)/status/$', StatusView.as_view(), name='problem-status'),
]
