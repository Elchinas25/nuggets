from django.shortcuts import render

from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from books.models import Review, Category
from .models import Votation


class VotationDetailView(DetailView):
	def get_queryset(self):
		return Votation.objects.all()


