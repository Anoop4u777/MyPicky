from django import forms
from .models import Item
from restaurants.models import RestaurantLocation

class ItemForm(forms.ModelForm):
	class Meta:
		model 	= Item
		fields 	=[
				'restaurants',
				'name',
				'contents',
				'excludes',
				'public'

				]

	def __init__(self, user=None, *args, **kwargs):  #get_form_kwargs() used in views
		super(ItemForm, self).__init__(*args, **kwargs)
		print(user)
		self.fields['restaurants'].queryset  = RestaurantLocation.objects.filter(user = user) #.exclude(item__isnull = False)
		""" .exclude(item__isnull = False) is used to remove the restaurant as we add items into it
		and if we want to show restaurants without items we use filter(user=user, item__isnull = True)"""
