from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import Chapter, Book, Category, Nugget, Review


class CategoryAdmin(TranslationAdmin):
    pass

class BookAdmin(TranslationAdmin):
    pass

class ChapterAdmin(TranslationAdmin):
    pass

class NuggetAdmin(TranslationAdmin):
    pass

class ReviewAdmin(TranslationAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Nugget, NuggetAdmin)
admin.site.register(Review, ReviewAdmin)
