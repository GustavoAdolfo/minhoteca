from django.shortcuts import render
from accounts.forms import CreateUserForm
from library.models import Book, Author


def index(request):
    authors_count = Author.objects.all().filter(
        book__is_available=True).distinct().count()
    books_count = Book.objects.filter(is_available=True).count()    
    form = CreateUserForm()
    context = {
        'form': form,
        'books_count': books_count,
        'authors_count': authors_count
    }
    return render(request, 'index.html', context)
