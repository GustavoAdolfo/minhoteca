from django.contrib import admin
from .models import Book, Author, Publisher, Borrowing


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'author_name', 'publisher_name',
                    'is_available', 'isbn')
    list_display_links = ('title',)
    list_per_page = 15
    list_filter = ('is_available', 'title', 'author_id__name')
    search_fields = ('title', 'subtitle', 'author_id__name', 'isbn')
    list_editable = ('is_available',)

    def author_name(self, obj):
        return obj.author.name
    def publisher_name(self, obj):
        return obj.publisher.name

    author_name.short_description = 'Author'
    author_name.admin_order_field = 'author_id__name'


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


class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'borrower_email', 'date_borrowed', 'date_returned')
    list_display_links = ('book_title', 'borrower_email')
    list_per_page = 15
    list_filter = ('borrower_id__email',)
    search_fields = ('book_id__title', 'borrower_id__email')

    def book_title(self, obj):
        return obj.book.title

    def borrower_email(self, obj):
        return obj.borrower.email

admin.site.register(Borrowing, BorrowingAdmin)
