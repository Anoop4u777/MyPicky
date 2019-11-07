# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db.models import Q

from django.conf import settings #Used for ForeginKey(User)

from .validators import validate_category, validate_email

from django.core.urlresolvers import reverse

from .utils import unique_slug_generator

from django.db.models.signals import pre_save

# Create your models here.

User = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.query.QuerySet): #the queryset value is here
	def search(self, query):			#RestaurantLocation.objects.all().search(query) OR RestaurantLocation.objects.filter(something).search()
		query = query.strip() # to remove empty spaces
		return self.filter(Q(Restaurant_Name__icontains = query)|
							Q(Restaurant_Location__icontains = query)|
							Q(Restaurant_Category__icontains = query) |
							Q(item__name__icontains = query)|
							Q(item__contents__icontains = query)|
							Q(item__contents__iexact = query)
							).distinct() #distinct used to avoid the same data multiple times(Just remove distinct and see)



class RestaurantLocationManager(models.Manager):  #This is created here because we can reuse it as search anywhere
	def get_queryset(self):
		return RestaurantLocationQuerySet(self.model, using = self._db) #using the same database(_db OR RestaurantLocation)

	def search(self, query): 		#RestaurantLocation.objects.search()
		return self.get_queryset().search(query)



class RestaurantLocation(models.Model):
		user 				= models.ForeignKey(User)
		Restaurant_Name 	= models.CharField(max_length=50, blank=False, null=False)
		Restaurant_Location	= models.CharField(max_length=50, blank=False, null=False)
		Restaurant_Category	= models.CharField(max_length=50, blank=False, null=False, validators =[validate_category])
		Restaurant_Email	= models.EmailField(blank=False, null=False, validators=[validate_email])
		Restaurant_Created	= models.DateTimeField(auto_now_add=True)
		Restaurant_Updated	= models.DateTimeField(auto_now=True)
		slug				= models.SlugField(blank=True, null=True)

		objects 			=RestaurantLocationManager() #similar to Model.objects.all().This shows the relation to this perticular RestaurantLocation model

		def __str__(self):
			return self.Restaurant_Name

		def get_absolute_url(self):
			return reverse('restaurants:detail', kwargs={'slug':self.slug})


def RL_pre_save_receiver(sender,instance,*args,**kwargs):	#to save and create slug used in unique
	if not instance.slug:									#slug generator utils.py
		instance.slug = unique_slug_generator(instance)


pre_save.connect(RL_pre_save_receiver , sender = RestaurantLocation)
