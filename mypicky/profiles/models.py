from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from .utils import code_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
# Create your models here.
User = settings.AUTH_USER_MODEL


class ProfileManager(models.Manager):
	def toggle_follow(self, request_user, username_to_toggle):
		profile_ = Profile.objects.get(user__username__iexact = username_to_toggle)
		user = request_user
		is_following = False
		if user in profile_.followers.all():
			profile_.followers.remove(user)
		else:
			profile_.followers.add(user)
			is_following = True
		print(user)
		return profile_, is_following


class Profile(models.Model):
	user 			= models.OneToOneField(User) #instead of using user.profile_set.all() we can use user.profile 
	followers 		= models.ManyToManyField(User, related_name = 'is_following', blank = True)	#user.followers.all() instead of user.profile_set.all()
	#following 	= models.ManyToManyField(User, related_name = 'following', blank = True) #user.following.all() instead of user.profile_set.all()
	activation_key	= models.CharField(max_length =120, blank =True, null = True )
	activated		= models.BooleanField(default= False)
	timestamp		= models.DateTimeField(auto_now_add= True)
	updated			= models.DateTimeField(auto_now= True)


	objects = ProfileManager()


	def __str__(self):
		return self.user.username

	def send_activation_email(self):
		if not self.activated:
			self.activation_key = code_generator()
			self.save()
			path_ = reverse('activate', kwargs = {'code': self.activation_key})
			subject = 'Activate Account'
			from_email = settings.DEFAULT_FROM_EMAIL
			message = 'Activate Your account here:{}'.format(path_)
			recipient_list = [self.user.email]
			html_message = '<p>Activate Your account here:{}</p>'.format(path_)
			sent_mail = False
			print(html_message)
			#sent_mail = send_mail(
			#			subject,
			#			message,
			#			from_email,
			#			recipient_list,
			#			fail_silently =	False,
			#			html_message = html_message	
			#			)
			return sent_mail



def post_save_user_reciever(sender, instance, created, *args, **kwargs):
	if created:
		profile, is_created	=Profile.objects.get_or_create(user= instance)
		default_user_profile =Profile.objects.get_or_create(user__id = 1)[0]
		default_user_profile.followers.add(instance)  #creating a default user to all new created ones
		profile.followers.add(default_user_profile.user) #to add users as default
		profile.followers.add(3)		#to add users as default


post_save.connect(post_save_user_reciever , sender = User)

