from django.conf.urls import include, url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.views.generic import TemplateView
from django.http import HttpResponse
from sttrbboy.users import views

urlpatterns = [
    url(r'^login/$', views.login, name="users|login"),
    url(r'^logout/$', views.logout, name="users|logout"),
    url(r'^contact/$', views.ContactPage.as_view(), name="contact"),
    url(r'^account/$', views.MyAccount.as_view(), name="users|account"),
    url(r'^register/$', views.RegisterUser.as_view(), name="users|register"),

    url(r'^password_reset/$', 
        password_reset, 
        {'post_reset_redirect' : '/users/password_reset_done/'},
        name="password_reset"),
    url(r'^password_reset_done/$',
        password_reset_done, name="password_reset_done"),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        password_reset_confirm, 
        {'post_reset_redirect' : '/users/password_done/'}, name="password_reset_confirm"),
    url(r'^password_done/$', 
        password_reset_complete),
]
