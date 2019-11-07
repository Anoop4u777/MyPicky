from django import forms

from .models import RestaurantLocation


class RestaurantCreateForm(forms.ModelForm):
		class Meta:
			model 	= RestaurantLocation
			fields 	= [
					'Restaurant_Name',
					'Restaurant_Location',
					'Restaurant_Category',
					'Restaurant_Email'
					]