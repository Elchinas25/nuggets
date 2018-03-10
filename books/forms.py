from .models import Review

from modeltranslation.forms import TranslationModelForm

class ReviewForm(TranslationModelForm):
	class Meta:
		model = Review
		fields = ['title', 'text', 'rating']


		
