from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse

from books.models import Book
from votations.models import Rating

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	followers		= models.ManyToManyField(User, related_name='following', blank=True)
	updated 		= models.DateField(auto_now=True)
	timestamp		= models.DateField(auto_now_add=True)
	timezone 		= models.CharField(max_length=120, blank=True, null=True)

	books_reviewed 	= models.ManyToManyField(Book, related_name='profiles_added_review')
	books_rated 	= models.ManyToManyField(Rating, related_name='profiles_added_rating')

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('profiles:detail', kwargs={'pk': self.pk})

def post_save_user_receiver(sender, instance, *args, **kwargs):
	profile = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)
