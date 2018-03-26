# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, FormView, TemplateView, UpdateView
from django.utils.decorators import method_decorator
from sttrbboy.users import forms
from sttrbboy.users.models import Profile
from datetime import timedelta
from django.http import HttpResponseRedirect

# Create your views here.


def login(request):
    return auth_views.login(request, "users/login.html")


def logout(request):
    return auth_views.logout(request, "/")


class RegisterUser(FormView):
    form_class = forms.UserRegistrationForm
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        return HttpResponseRedirect("/")

    def get_context_data(self, **kwargs):
        return super(RegisterUser, self).get_context_data(**kwargs)


class ContactPage(TemplateView):
    template_name = "users/contact.html"

    def get_context_data(self, **kwargs):
        return super(ContactPage, self).get_context_data(**kwargs)


class ResetPassword(FormView):
    form_class = PasswordResetForm
    template_name = "users/reset_password.html"

    def form_valid(self, form):
        form.save(request=self.request)
        messages.sucess(self.request, "Password changed successfully.")
        return HttpResponseRedirect("/")


class MyAccount(UpdateView):
    form_class = forms.ProfileForm
    template_name = "users/account.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MyAccount, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Account settings updated successfully.")
        return super(MyAccount, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MyAccount, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
