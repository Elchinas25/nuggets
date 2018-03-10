from django.db import models

# Create your models here.
from django.db import models

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models.signals import pre_save
from django.urls import reverse
from django.db.models import Q

from votations.models import Votation, Rating

from .utils import unique_slug_generator

User = settings.AUTH_USER_MODEL


class Category(models.Model):
	title = models.CharField(max_length=120, blank=False, null=False)
	slug = models.SlugField(blank=True, null=True, editable=False)

	class Meta:
		verbose_name_plural = "categories"

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('books:category_detail', kwargs = {'pk': self.pk})

# class EnglishReviews(models.Manager):
# 	def get_queryset(self):
# 		return self.object.review_set.all().filter(language='en')

# class SpanishReviews(models.Manager):
# 	def get_queryset(self):
# 		return self.object.review_set.all().filter(language='es')


class BookQuerySet(models.QuerySet):
	def search(self, query, category):
		obj = self.filter(category__slug__iexact=category).filter(
				Q(author__icontains=query) |
				Q(title__icontains=query)
				)

		if len(obj) == 0:
			return None
		else:
			return obj

class BookCustomManager(models.Manager):
	def get_queryset(self):
		return BookQuerySet(self.model, using=self.db)

	def search(self, query, category):
		return self.get_queryset().search(query, category)

class Book(models.Model):
	category 	= models.ManyToManyField(Category, related_name='books')
	rating_model = models.OneToOneField(Rating, blank=True, null=True, editable=False)
	votation    = models.ForeignKey(Votation, on_delete=models.CASCADE, null=True)

	title 		= models.CharField(max_length=120, blank=False, null=False)
	active		= models.BooleanField(default=False)
	description = models.TextField(max_length=500)
	slug 		= models.SlugField(blank=True, null=True, editable=False)
	image 		= models.ImageField(upload_to='books', blank=True, null=True)
	url 		= models.URLField(max_length=200, blank=True, null=True)
	author 		= models.CharField(max_length=120, blank=True, null=True)
	timestamp 	= models.DateField(auto_now_add=True, editable=False)
	updated 	= models.DateField(auto_now=True, editable=False)
	date 		= models.DateField(blank=True, null=True)

	objects 		= models.Manager()
	search_manager  = BookCustomManager()

	class Meta:
		ordering = ['-rating_model__average']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('books:book_detail', kwargs = {'slug': self.slug})


class Chapter(models.Model):
	book 	= models.ForeignKey(Book, on_delete=models.CASCADE, blank=False, null=False)
	title 	= models.CharField(max_length=120, blank=False, null=False)
	slug 	= models.SlugField(blank=True, null=True, editable=False)

	def __str__(self):
		return self.title

class Nugget(models.Model):
	user 		  = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
	book 		  = models.ForeignKey(Book, on_delete=models.CASCADE, blank=False, null=False)
	chapter 	  = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=True, null=True)

	title 		  = models.CharField(max_length=160, blank=False, null=False)
	description	  = models.TextField(max_length=350, blank=True, null=True)
	active		  = models.BooleanField(default=False)
	rating		  = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)
	slug 		  = models.SlugField(blank=True, null=True, editable=False)
	timestamp 	  = models.DateField(auto_now_add=True, blank=True, null=True, editable=False)

	ratings		= []
	average 	= models.FloatField(default=5)

	class Meta:
		ordering = ['-average']

	def __str__(self):
		return self.title

	def rate(self, vote):
		self.ratings.append(float(vote))
		self.average = sum(self.ratings)/float(len(self.ratings))
		self.save()


# class EnglishReviews(models.Manager):
# 	def get_queryset(self):
# 		return super().get_queryset().filter(language='en')

# class SpanishReviews(models.Manager):
# 	def get_queryset(self):
# 		return super().get_queryset().filter(language='es')

class Review(models.Model):
	user 		= models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
	book 		= models.ForeignKey(Book, on_delete=models.CASCADE, blank=False, null=False)

	title		= models.CharField(max_length=160, blank=False, null=True)
	text 		= models.TextField(max_length=500, blank=False, null=False)
	rating 		= models.IntegerField(blank=False, null=False)
	timestamp 	= models.DateField(auto_now_add=True, null=True)

	#puntuation  = models.IntegerField(null=True)

	SPANISH		= 'es'
	ENGLISH 	= 'en'
	ALL 		= 'all'

	LANGUAGE_CHOICES = (
		(SPANISH, 'Spanish'), 
		(ENGLISH, 'English'),
		(ALL, 'All')
		)

	language = models.CharField(max_length=120, choices=LANGUAGE_CHOICES, default=ENGLISH)

	def __str__(self):
		return 'review for "{:s}" by {:s}'.format(self.book.title, self.user.username)



def pre_save_category_receiver(sender, instance, *args, **kwargs):
	instance.slug = unique_slug_generator(instance)

def pre_save_book_receiver(sender, instance, *args, **kwargs):
	instance.slug = unique_slug_generator(instance)
	try:
		rating_model = Rating.objects.get(book=instance)
	except:
		new_rating_model = Rating.objects.create()
		instance.rating_model = new_rating_model

def pre_save_chapter_receiver(sender, instance, *args, **kwargs):
	instance.slug = unique_slug_generator(instance)

def pre_save_nugget_receiver(sender, instance, *args, **kwargs):
	instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_category_receiver, sender=Category)
pre_save.connect(pre_save_book_receiver, sender = Book)
pre_save.connect(pre_save_chapter_receiver, sender = Chapter)
pre_save.connect(pre_save_nugget_receiver, sender = Nugget)




