from django.conf.urls import include, url
from django.views.generic import TemplateView

from sttrbboy.hunt.views import *


urlpatterns = [
    url(r'^$', ListHunts.as_view(), name='hunt|list'),
    url(r'^hunt/(?P<pk>[0-9]+)/$', ShowHunt.as_view(), name='hunt|show'),
    url(r'^page/(?P<pk>[0-9]+)/$', ShowPage.as_view(), name='page|show'),
    url(r'^item/(?P<pk>[0-9]+)/$', ShowItem.as_view(), name='item|show'),
    url(r'^item/(?P<pk>[0-9]+)/newcomment$', MakeNewComment.as_view(), name="new|comment"),
    url(r'hunt/(?P<pk>[0-9]+)/list_items/$', ShowItems.as_view(), name="hunt|list_items"),
    url(r'hunt/(?P<pk>[0-9]+)/list_my_items/$', ShowMyItems.as_view(), name="hunt|list_my_items"),
]
