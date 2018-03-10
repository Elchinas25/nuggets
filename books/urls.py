from django.conf.urls import url
from django.contrib import admin

from django.conf.urls.i18n import i18n_patterns

from .views import CategoryListView, CategoryDetailView, BookDetailView, Reviews, CategoryAll

urlpatterns = [
	url(r'^categories/$', CategoryListView.as_view(), name='categories'),
	url(r'^categories/(?P<pk>\d)/$', CategoryDetailView.as_view(), name='category_detail'),
	url(r'^categories/(?P<pk>\d)/all/$', CategoryAll.as_view(), name='category_all'),
	url(r'^(?P<slug>[\w-]+)/$', BookDetailView.as_view(), name='book_detail'),
	url(r'^(?P<slug>[\w-]+)/reviews/$', Reviews.as_view(), name='reviews'),
	# url(r'^reviews/add/$', CreateReview.as_view(), name='create_review'),
	# url(r'^(?P<slug>[\w-]+)/$', BookDetailView.as_view(), name='book_detail'),
]