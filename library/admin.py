from django.contrib import admin
from .models import Book, Author, Publisher


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'author_name',
                    'is_available', 'isbn')
    list_display_links = ('title',)
    list_per_page = 15
    list_filter = ('title', 'subtitle', 'author_id__name', 'is_available')
    search_fields = ('title', 'subtitle', 'author', 'isbn')
    list_editable = ('is_available',)

    def author_name(self, obj):
        return obj.author.name

    author_name.short_description = 'Author'
    author_name.admin_order_field = 'book__author'


admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_display_links = ('name',)
    list_per_page = 15
    list_filter = ('name', 'country')
    search_fields = ('name', 'country')


admin.site.register(Author, AuthorAdmin)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    list_display_links = ('name',)
    list_per_page = 15
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Publisher, PublisherAdmin)
