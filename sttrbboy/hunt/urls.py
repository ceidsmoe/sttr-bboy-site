from django.conf.urls import include, url
from django.views.generic import TemplateView

from sttrbboy.hunt.views import *


urlpatterns = [
    url(r'^$', ListHunts.as_view(), name='hunt|list'),
    url(r'^hunt/(?P<pk>[0-9]+)/$', ShowHunt.as_view(), name='hunt|show'),

    url(r'^hunt/(?P<huntpk>[0-9]+)/page/(?P<pk>[0-9]+)/$', ShowPage.as_view(), name='page|show'),
    url(r'^hunt/(?P<huntpk>[0-9]+)/roadtrip_page/(?P<pk>[0-9]+)/$', ShowPage.as_view(), name='roadtrippage|show'),
    url(r'^hunt/(?P<huntpk>[0-9]+)/olympics_page/(?P<pk>[0-9]+)/$', ShowPage.as_view(), name='olympicspage|show'),

    url(r'^hunt/(?P<huntpk>[0-9]+)/item/(?P<pk>[0-9]+)/$', ShowItem.as_view(), name='item|show'),
    url(r'^hunt/(?P<huntpk>[0-9]+)/item/(?P<pk>[0-9]+)/newcomment$', MakeNewComment.as_view(), name="new|comment"),

    url(r'^hunt/(?P<huntpk>[0-9]+)/roadtrip_item/(?P<pk>[0-9]+)/$', ShowItem.as_view(), name='roadtripitem|show'),
    url(r'^hunt/(?P<huntpk>[0-9]+)/roadtrip_item/(?P<pk>[0-9]+)/newcomment$', MakeNewComment.as_view(), name="roadtripnew|comment"),

    url(r'^hunt/(?P<huntpk>[0-9]+)/olympics_item/(?P<pk>[0-9]+)/$', ShowItem.as_view(), name='olympicsitem|show'),
    url(r'^hunt/(?P<huntpk>[0-9]+)/olympics_item/(?P<pk>[0-9]+)/newcomment$', MakeNewComment.as_view(), name="olympicsnew|comment"),

    url(r'hunt/(?P<pk>[0-9]+)/list_items/$', ShowItems.as_view(), name="hunt|list_items"),
    url(r'hunt/(?P<pk>[0-9]+)/list_my_items/$', ShowMyItems.as_view(), name="hunt|list_my_items"),

    url(r'scavvie/(?P<pk>[0-9]+)/$', ShowScavvie.as_view(), name='scavvie|show'),
    url(r'hunt/(?P<pk>[0-9]+)/scavvie_directory/$',ScavvieDirectory.as_view(), name='hunt|scavvie_directory'),
]
