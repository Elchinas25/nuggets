from django.shortcuts import render

from django.views.generic import View, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from django.http import HttpResponse

from django.db.models import Count
from django.db.models import Q

from votations.models import Votation

from .models import Chapter, Book, Category, Nugget, Review
from .forms import ReviewForm




class CategoryListView(ListView):
	template_name = 'books/categories.html'

	def get_queryset(self):
		return Category.objects.all()


class CategoryDetailView(DetailView):
	template_name = 'books/category_detail.html'

	def get_queryset(self):
		return Category.objects.all().annotate(n_books = Count('books'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		obj = kwargs['object']

		# current_votations = Votation.objects.get(Q(category=obj) & Q(active=True))
		# context['votations'] = current_votations

		return context


def sorter(obj, state, fields):
	if state == 'active':
		active = True
	elif state == 'unactive':
		active = False
	else:
		active = None

	if fields == 'newest':
		date = '-date'
	elif fields == 'oldest':
		date = 'date'
	else:
		date = None

	if active != None:
		if date != None:
			qs = obj.books.filter(active=active).order_by(date)
		else:
			qs = obj.books.filter(active=active)
	else:
		if date != None:
			qs = obj.books.all().order_by(date)
		else:
			qs = obj.books.all()

	return qs



class CategoryAll(DetailView):
	template_name = 'books/category_all.html'

	def get_queryset(self):
		return Category.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)

		obj = kwargs['object']
		query = self.request.GET.get('query')
		
		if query:
			books = Book.search_manager.search(query, obj.slug)

			if books == None:
				context['error_message'] = 'Sorry, no matches for "{}"'.format(query)
			else:
				context['books'] = books
				context['is_valid'] = True
		else:
			sort_state = self.request.GET.get('sort_state')
			sort_fields = self.request.GET.get('sort_fields')
			
			if sort_state == 'all' and sort_fields == 'rating' or sort_state==None and sort_fields==None:
				context['books'] = obj.books.all()
			else:
				context['books'] = sorter(obj, sort_state, sort_fields)

			print(sort_state)
			print(sort_fields)

		return context

	# def get(self, *args, **kwargs):
	# 	query = self.request.GET.get('query')
	# 	print(query)



class BookDetailView(DetailView):
	def get_queryset(self):
		return Book.objects.annotate(n_reviews=Count('review'))

	def post(self, *args, **kwargs):
		rating = int(self.request.POST.get('rating_form'))
		user = self.request.user

		self.object = self.get_object(self.get_queryset()) 
		self.object.rating_model.rate(vote=rating, user=user)

		ctx = self.get_context_data(**kwargs)
		ctx['message'] = 'Your rating has been saved, thanks!'

		return render(self.request, 'books/book_detail.html', ctx)



class Reviews(DetailView):
	template_name = 'books/reviews.html'
	def get_queryset(self):
		return Book.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		if get_language() == 'es':
			context['reviews'] = self.object.review_set.all().filter(Q(language='es') | Q(language='all'))
		else:
			context['reviews'] = self.object.review_set.all().filter(Q(language='en') | Q(language='all'))

		context['form'] = ReviewForm()

		return context

	def post(self, *args, **kwargs):
		self.object = self.get_object(self.get_queryset())
		context = self.get_context_data(**kwargs)

		data = self.request.POST
		print(data)
		user = self.request.user
		form = ReviewForm(data)
		

		if form.is_valid():
			obj = form.save(commit=False)
			obj.book = self.object
			obj.user = user
			obj.language = get_language()
			obj.save()
			context['message'] = 'Your review has been successfully saved! Thanks for your help to the community.'

			user.profile.books_reviewed.add(self.object)
			# self.object.rating_model.rate(int(data['rating']))

			return render(self.request, 'books/reviews.html', context)

		else:
			context.update({'form': form})
			return render(self.request, 'books/reviews.html', context)

	






	

# class CreateReview(CreateView):
# 	template_name = 'books/create_review.html'
# 	form_class = ReviewForm

# 	def form_valid(self, form):
# 		obj = form.save(commit=False)
# 		return super().form_valid(form)

# class BookLoc(CreateView):
# 	template_name = 'books/book_detail.html'
# 	form_class = ReviewForm
# 	success_url = '/books/categories/'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super().get_context_data(*args, **kwargs)

# 		slug = self.kwargs.get('slug')
# 		obj = Book.objects.get(slug__iexact=slug)

# 		if get_language() == 'es':
# 			context['reviews'] = obj.review_set.all().filter(language__iexact='es')
# 		else:
# 			context['reviews'] = obj.review_set.all().filter(language__iexact='en')

# 		if len(context['reviews']) == 0:
# 			context['is_empty'] = True

# 		context['object'] = obj
# 		return context

# 	def form_valid(self, form):
# 		obj = form.save(commit=False)

# 		return super().form_valid(form)

# 	def get_form_kwargs(self, *args, **kwargs):
# 		kwargs = super().get_form_kwargs(*args, **kwargs)
# 		kwargs['user'] = self.request.user
# 		# kwargs['book'] = 
# 		kwargs['language'] = get_language()

# 		return kwargs
