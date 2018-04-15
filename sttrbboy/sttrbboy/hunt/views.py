# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import *
from django.conf import settings
from django.db import transaction
from django.db.models.expressions import RawSQL
from django.contrib import messages
from django.http import *
from django.core.exceptions import *
from django.views.generic import *
from django.views.generic.edit import BaseFormView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import *
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from sttrbboy.hunt.models import *
from sttrbboy.users.models import *
from sttrbboy.hunt.forms import *

# Create your views here.
class ListHunts(ListView):
	model = Hunt
	template_name = 'hunt/list.html'

class ShowHunt(DetailView):
	model = Hunt
	template_name = 'hunt/show.html'

	def get_context_data(self, **kwargs):
		context = super(ShowHunt, self).get_context_data(**kwargs)
		if self.object.status in ('in_progress', 'finished'):
			if self.object.items.count() > 0:
				context['items'] = self.object.items.all()

			if self.object.pages.count() > 0:
				context['pages'] = self.object.pages.all()

				
		if self.request.user.is_authenticated():
			in_hunt = Scavvie.objects.filter(hunt=self.object, user=self.request.user).exists()
			if in_hunt:
				scavvie = Scavvie.objects.get(hunt=self.object, user=self.request.user)
				context['scavvie'] = scavvie


				if self.object.status in ('in_progress', 'finished'):
					pass
		return context


class ShowPage(DetailView):
	model = Page
	template_name = 'hunt/show_page.html'

	def get_context_data(self, **kwargs):
		context = super(ShowPage, self).get_context_data(**kwargs)
		if self.object.items.count() > 0:
			context['items'] = self.object.items.all()
		else:
			context['items'] = None

		return context


class RegisterForHunt(FormView):
	form_class = HuntRegistrationForm
	template_name = "hunt/register.html"

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		self.hunt = get_object_or_404(Hunt, id=self.kwargs['pk'])
		if Scavvie.objects.filter(hunt=self.hunt, user=request.user).exists():
			return HttpResponseRedirect(self.hunt.get_absolute_url())
		return super(RegisterForHunt, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		scavvie = form.save(commit=False)
		scavvie.user = self.request.user
		scavvie.hunt = self.hunt
		scavvie.save()
		messages.success(self.request, "You are now registered for the %d Scav Hunt!" % (self.hunt.year))
		return HttpResponseRedirect(self.hunt.get_absolute_url())

	def get_context_data(self, **kwargs):
		context = super(RegisterForHunt, self).get_context_data(**kwargs)
		context['hunt'] = self.hunt
		return context

	def get_form_kwargs(self):
		kwargs = super(RegisterForHunt, self).get_form_kwargs()
		kwargs['hunt'] = self.hunt
		return kwargs