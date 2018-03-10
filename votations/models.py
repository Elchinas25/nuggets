import json
import operator

from django.db import models
from django.db.models.signals import pre_save
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

import books


class Votation(models.Model):
	category 	= models.ForeignKey('books.Category', on_delete=models.CASCADE, null=True)

	timestamp 	= models.DateField(auto_now_add=True, editable=False)

	active		= models.NullBooleanField(default=False, blank=True)
	finished 	= models.NullBooleanField(default=False, blank=True)

	start_week  = models.DateTimeField(null=True)
	start_vots  = models.DateTimeField(null=True)
	end_week 	= models.DateTimeField(null=True)

	puntuations	= JSONField(blank=True, null=True, editable=True)

	ORDER = (
			('1', _('First')),
			('2', _('Second')),
			('3', _('Third')),
		)

	# month  		= models.CharField(max_length=4, choices=MONTHS, null=True)
	position	= models.CharField(max_length=2, choices=ORDER, null=True)


	def __str__(self):
		return "{}. {} {}".format(self.category.title, self.get_position_display(), _('votation for'))

	def get_absolute_url(self):
		return reverse('votations:votation_detail', kwargs = {'pk': self.pk})

	def add_book(self, book):
		self.puntuations[book.slug] = str(0)

		self.book_set.add(book)
		self.save()

	def puntuate_book(self, book, puntuation):
		book_puntuation = json.loads(self.puntuations[book.slug])

		if puntuation == 'like': 
			book_puntuation += 1
		elif puntuation == 'dislike':
			book_puntuation -= 1

		self.puntuations[book.slug] = json.dumps(book_puntuation)
		self.save()

	def get_ordered(self):
		puntuations = self.puntuations

		for k, v in puntuations.items():
			puntuations[k] = int(v)

		sorted_punts = sorted(puntuations.items(), key=operator.itemgetter(1), reverse=True)

		books_ordered = []

		for t in sorted_punts:
			book = books.models.Book.objects.get(slug__iexact=t[0])
			books_ordered.append(book) 

		return books_ordered

	def get_winners(self):
		ordered = self.get_ordered()

		winner = ordered[0]
		almost_winners = ordered[1:4]

		return winner, almost_winners






class Rating(models.Model):
	ratings		= JSONField(null=True, editable=True)
	average 	= models.FloatField(default=5)

	def rate(self, vote, user):
		numbers = json.loads(self.ratings['numbers'])

		numbers.append(float(vote))
		self.average = sum(numbers)/float(len(numbers))

		self.ratings['numbers'] = json.dumps(numbers)
		self.save()

		user.profile.books_rated.add(self)

	def __str__(self):
		return 'Rating model for: "{}"'.format(self.book.title)




def pre_save_rating_receiver(sender, instance, *args, **kwargs):
	if not instance.ratings:
		instance.ratings = {'numbers': '[5]'}

def pre_save_votation_receiver(sender, instance, *args, **kwargs):
	if not instance.puntuations:
		instance.puntuations = {}

pre_save.connect(pre_save_rating_receiver, sender=Rating)
pre_save.connect(pre_save_votation_receiver, sender=Votation)







# MONTHS = (
	# 		('ja', _('January')),
	# 		('fe', _('February')),
	# 		('ma', _('March')),
	# 		('ap', _('April')),
	# 		('may', _('May')),
	# 		('ju', _('June')),
	# 		('jul', _('July')),
	# 		('au', _('August')),
	# 		('se', _('September')),
	# 		('oc', _('October')),
	# 		('no', _('November')),
	# 		('de', _('December')),
		# )


# from votations.models import Votation
# v = Votation.objects.first()
# v.book_set.all()
# from books.models import Book
# b = Book.objects.first()