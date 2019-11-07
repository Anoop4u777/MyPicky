from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View
from .models import Item
from .forms import ItemForm
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return render(request, 'restaurants/HomePage.html', {})
		user = request.user
		is_following_user_ids = [x.user.id for x in user.is_following.all()] # list of users
		qs = Item.objects.filter(user__id__in = is_following_user_ids, public = True).order_by('-updated')[:3]
		return render(request, 'menus/home-feed.html', {'object_list':qs})
		

class ItemListView(LoginRequiredMixin, ListView):
	login_url = "/login/"
	
	def get_queryset(self):
		return Item.objects.filter(user = self.request.user)


class ItemDetailView(LoginRequiredMixin, DetailView):
	login_url = "/login/"
	
	def get_queryset(self):
		return Item.objects.filter(user = self.request.user)



class ItemCreateView(LoginRequiredMixin, CreateView):
	template_name = "form.html" 
	form_class = ItemForm
	login_url = "/login/" 
	
	def get_queryset(self): # to get the queryset according to the user
		return Item.objects.filter(user = self.request.user)

	def form_valid(self, form): #to get the form according to the user
		instance = form.save(commit = False)
		instance.user = self.request.user
		return super(ItemCreateView, self).form_valid(form)

	def get_form_kwargs(self):  # passing values to form class using the foreignkey(To get the restaurant list in Html)
		kwargs = super(ItemCreateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs


	def get_context_data(self, *args, **kwargs): #to get the context data as well as add title
		context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = "Add Items"
		return context

class ItemUpdateView(LoginRequiredMixin, UpdateView):
	template_name = "menus/update-detail.html"
	form_class = ItemForm
	login_url = "/login/" 
	
	def get_queryset(self):
		return Item.objects.filter(user = self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = "Update Items"
		return context

	def get_form_kwargs(self):  # passing values to form class using the foreignkey(To get the restaurant list in Html)
		kwargs = super(ItemUpdateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

