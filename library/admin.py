from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'author', 'is_available', 'isbn')
    list_display_links = ('title',)
    list_per_page = 15
    list_filter = ('title', 'subtitle', 'author', 'is_available')
    search_fields = ('title', 'subtitle', 'author', 'isbn')
    list_editable = ('is_available',)


admin.site.register(Book, BookAdmin)
