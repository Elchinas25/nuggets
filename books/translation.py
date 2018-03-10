from modeltranslation.translator import translator, TranslationOptions
from .models import Book, Chapter, Category, Nugget, Review


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class ChapterTranslationOptions(TranslationOptions):
    fields = ('title',)

class NuggetTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class ReviewTranslationOptions(TranslationOptions):
    fields = ('text', 'title',)

translator.register(Category, CategoryTranslationOptions)
translator.register(Book, BookTranslationOptions)
translator.register(Chapter, ChapterTranslationOptions)
translator.register(Nugget, NuggetTranslationOptions)
translator.register(Review, ReviewTranslationOptions)