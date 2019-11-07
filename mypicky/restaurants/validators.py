from django.core.exceptions import ValidationError




"""def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
"""

category = ['Vegiterian','Non-Vegiterian','Vegiterian and Non-Vegiterian','Chineese',]

def validate_category(value):

	if not value in category:
		raise ValidationError("Not a valid category!!")






def validate_email(value):

	if '.edu' in value:
		raise ValidationError("Not a valid Email Id !!")
	if '.yahoo.com' in value:
		raise ValidationError("We dont accept Yahoo Mail Id !!")

 