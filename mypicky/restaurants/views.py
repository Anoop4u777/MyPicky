# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .forms import RestaurantCreateForm

from .models import RestaurantLocation

from django.views.generic import CreateView,UpdateView,ListView,DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class RestaurantCreate(LoginRequiredMixin, CreateView):
	template_name 	= "form.html" 
	form_class 		= RestaurantCreateForm
	login_url 		= "/login/" 
	

	def form_valid(self, form):
		instance 		= form.save(commit=False)
		instance.user 	= self.request.user   		
		return super(RestaurantCreate , self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context 			= super(RestaurantCreate, self).get_context_data(*args, **kwargs)
		context['title'] 	= 'Add Restaurants'
		return context

class RestaurantUpdate(LoginRequiredMixin, UpdateView):
	template_name 	= "restaurants/detail-update.html" 
	form_class 		= RestaurantCreateForm
	login_url 		= "/login/" 
	

	def get_context_data(self, *args, **kwargs):
		context 		 = super(RestaurantUpdate, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Restaurants'
		return context

	def get_queryset(self):
		return RestaurantLocation.objects.filter(user = self.request.user)

	
class RestaurantList(LoginRequiredMixin, ListView):
	template_name = "restaurants/RestaurantList.html/"
	login_url 	  = "/login/"
	
	def get_queryset(self):
		return RestaurantLocation.objects.filter(user = self.request.user)
	


class RestaurantDetail(LoginRequiredMixin, DetailView):
	template_name 	  = "restaurants/RestaurantDetail.html/"
	login_url 		  = "/login/"

	def get_queryset(self):
		return RestaurantLocation.objects.filter(user = self.request.user)

