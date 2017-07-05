from django.conf.urls import url
from .views import SubmissionView

app_name = 'submissions'

urlpatterns = [
    url(r'^(?P<sid>[.\-_\w]+)/$', SubmissionView.as_view(), name='submission'),
]
