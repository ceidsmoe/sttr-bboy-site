from django.conf.urls import include, url
from django.views.generic import TemplateView

from sttrbboy.hunt.views import *


urlpatterns = [
    url(r'^$', ListHunts.as_view(), name='hunt|list'),
    url(r'^hunt/(?P<pk>[0-9]+)/$', ShowHunt.as_view(), name='hunt|show'),
    #url(r'^hunt/(?P<pk>[0-9]+)/register/$', RegisterForHunt.as_view(), name='hunt|register'),
]
