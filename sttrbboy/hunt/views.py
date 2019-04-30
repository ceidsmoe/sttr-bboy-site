# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import *
from django.conf import settings
from django.db import transaction
from django.db.models import Q
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
from django.urls import reverse

from sttrbboy.hunt.models import *
from sttrbboy.users.models import *
from sttrbboy.hunt.forms import *


# Create your views here.
class ListHunts(ListView):
	model = Hunt
	template_name = 'hunt/list.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			my_profile = Profile.objects.get_or_create(user=request.user)[0]
			if my_profile.name == "" or my_profile.gender_pronouns == "":
				return HttpResponseRedirect(reverse("users|account"))

		return super(ListHunts, self).dispatch(request, *args, **kwargs)


class ShowHunt(DetailView):
	model = Hunt
	template_name = 'hunt/show.html'

	def get_context_data(self, **kwargs):
		context = super(ShowHunt, self).get_context_data(**kwargs)
		if self.object.status in ('in_progress', 'finished'):
			if self.object.items.count() > 0:
				number_done = sum([1 for i in self.object.items.all() if i.completed])
				context['percentage_done'] = int(float(number_done) / self.object.items.count() * 100)
			else:
				context['percentage_done'] = 0

			context['items'] = self.object.items.all()
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

	def dispatch(self, request, *args, **kwargs):
		is_olympics = "olympics" in request.path
		is_roadtrip = "roadtrip" in request.path

		self.hunt = get_object_or_404(Hunt, id=self.kwargs['huntpk'])

		if Page.objects.filter(number=self.kwargs['pk'], hunt=self.hunt).count() > 1:
			self.page = get_object_or_404(Page, number=self.kwargs['pk'], hunt=self.hunt, olympics=is_olympics, roadtrip=is_roadtrip)
		else:	
			self.page = get_object_or_404(Page, number=self.kwargs['pk'], hunt=self.hunt)

		self.kwargs['pk'] = self.page.pk
		
		return super(ShowPage, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ShowPage, self).get_context_data(**kwargs)
		context['items'] = self.page.items.all()
		return context


class ShowItem(UpdateView):
	form_class = ItemForm
	model = Item
	template_name = 'hunt/show_item.html'

	def get_context_data(self, **kwargs):
		context = super(ShowItem, self).get_context_data(**kwargs)
		context['interested_scavvies'] = self.object.interested_scavvies.all()
		context['comments'] = self.object.comments.all()
		context['item_interested'] = self.scavvie in context['interested_scavvies']
		context['item_working'] = self.scavvie in self.object.working_scavvies.all()
		context['item_complete'] = self.object.completed
		return context

	def dispatch(self, request, *args, **kwargs):
		self.hunt = get_object_or_404(Hunt, id=self.kwargs['huntpk'])

		is_olympics = "olympics" in request.path
		is_roadtrip = "roadtrip" in request.path

		if Item.objects.filter(number=self.kwargs['pk']).count() > 1:
			self.item = get_object_or_404(Item, number=self.kwargs['pk'], hunt=self.hunt, roadtrip=is_roadtrip, olympics=is_olympics)
		else:
			self.item = get_object_or_404(Item, number=self.kwargs['pk'], hunt=self.hunt)
		if not request.user.is_authenticated():
			self.scavvie = None
		elif Scavvie.objects.filter(hunt=self.item.hunt, user=request.user).exists():
			self.scavvie = get_object_or_404(Scavvie, hunt=self.item.hunt, user=request.user)
		else:
			self.scavvie = None

		self.kwargs['pk'] = self.item.pk

		return super(ShowItem, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		if form.interested:
			if self.scavvie in self.object.interested_scavvies.all():
				self.item.interested_scavvies.remove(self.scavvie)
			else:
				self.item.interested_scavvies.add(self.scavvie)
		if form.working:
			if self.scavvie in self.object.working_scavvies.all():
				self.item.working_scavvies.remove(self.scavvie)
			else:
				self.item.working_scavvies.add(self.scavvie)
				self.item.started = True
		if form.completed:
			if not self.item.completed:
				self.item.completed_scavvies.add(self.scavvie)
			else:
				self.item.completed_scavvies.remove(self.scavvie)
			self.item.completed = not self.item.completed

		self.item.save()
		messages.success(self.request, "Item updated")
		return HttpResponseRedirect(self.item.get_absolute_url())


class MakeNewComment(FormView):
	form_class = ItemCommentForm
	template_name = "hunt/new_comment.html"

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		is_olympics = "olympics" in request.path
		is_roadtrip = "roadtrip" in request.path

		self.hunt = get_object_or_404(Hunt, id=self.kwargs['huntpk'])
		self.scavvie = get_object_or_404(Scavvie, hunt=self.hunt, user=request.user)

		if Item.objects.filter(number=self.kwargs['pk']).count() > 1:
			self.item = get_object_or_404(Item, number=self.kwargs['pk'], hunt=self.hunt, roadtrip=is_roadtrip, olympics=is_olympics)
		else:
			self.item = get_object_or_404(Item, number=self.kwargs['pk'], hunt=self.hunt)

		return super(MakeNewComment, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.item = self.item
		comment.scavvie = self.scavvie
		comment.save()
		messages.success(self.request, "Your comment on item %d has been posted!" % (self.item.number))
		return HttpResponseRedirect(self.item.get_absolute_url())



class ShowItems(ListView):
	template_name = "hunt/list_items.html"
	model = Item

	def dispatch(self, request, *args, **kwargs):
		self.hunt = get_object_or_404(Hunt, id=self.kwargs['pk'])
		return super(ShowItems, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ShowItems, self).get_context_data(**kwargs)
		context['tags'] = [it.title for it in Tag.objects.all()]
		context['items'] = Item.objects.filter(hunt=self.hunt)
		return context

class ShowMyItems(ListView):
	template_name = "hunt/list_my_items.html"
	model = Item

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		self.hunt = get_object_or_404(Hunt, id=self.kwargs['pk'])
		self.scavvie = get_object_or_404(Scavvie, user=request.user, hunt=self.hunt)
		return super(ShowMyItems, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ShowMyItems, self).get_context_data(**kwargs)
		context['items'] = Item.objects.filter(Q(hunt=self.hunt), Q(interested_scavvies=self.scavvie) | Q(working_scavvies=self.scavvie) | Q(completed_scavvies=self.scavvie) | Q(page_captain=self.scavvie))
		context['tags'] = [it.title for it in Tag.objects.all()]
		return context

class ShowScavvie(DetailView):
	template_name = "hunt/show_scavvie.html"
	model = Scavvie

class ScavvieDirectory(ListView):
	template_name = "hunt/scavvie_directory.html"
	model = Scavvie

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		self.hunt = get_object_or_404(Hunt, id=self.kwargs['pk'])
		return super(ScavvieDirectory, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ScavvieDirectory, self).get_context_data(**kwargs)
		context['scavvies'] = Scavvie.objects.filter(hunt=self.hunt)
		return context