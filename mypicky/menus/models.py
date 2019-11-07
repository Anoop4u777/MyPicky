from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from restaurants.models import RestaurantLocation

class Item(models.Model):
	#Associations which connect a perticular user and a perticular location
	user			=	models.ForeignKey(settings.AUTH_USER_MODEL)
	restaurants		=	models.ForeignKey(RestaurantLocation)
	#Items in the Item Model
	name			=	models.CharField(max_length=120)
	contents		=	models.TextField(help_text='Each Item separated by comma')
	excludes		=	models.TextField(blank = True, null = True, help_text='Each Item separated by comma')
	public			=	models.BooleanField(default = True)
	time_created	=	models.DateTimeField(auto_now_add = True)
	updated			=	models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ['-updated','-time_created']  #to show which item is updated last in the begining of the list

	def __str__(self):
		return self.name

	def get_absolute_url(self):
			return reverse('menus:detail', kwargs={'pk':self.pk})



	def get_contents(self):			#To get comma between the contents
		return self.contents.split(",")

	def get_excludes(self):
		return self.excludes.split(",")