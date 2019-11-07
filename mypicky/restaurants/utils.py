#random string generator which is used in urls is created here

import random
import string

from django.utils.text import slugify

#slugify--django inbuilt slug generator

"""Here we create a random unique slug just like pk or id which 
can be used to access to a specific content with this slug generated"""

Dont_use = ['create'] #no need to create slug insid e create view


def random_string_generator(size=10,chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance,new_slug=None):


	if new_slug is not None:
		slug = new_slug
	else :
		slug = slugify(instance.Restaurant_Name)
	if slug in Dont_use:
		new_slug = "{slug}-{randstr}".format(
							slug=slug,
							randstr = random_string_generator(size=4)
						)
		return unique_slug_generator(instance, new_slug=new_slug)
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(slug=slug).exists()
	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
							slug=slug,
							randstr = random_string_generator(size=4)
						)
		return unique_slug_generator(instance, new_slug=new_slug)
	return slug