from datetime import datetime
from django.shortcuts import render
from django.db.models import Q
from accounts.forms import CreateUserForm
from accounts.models import MinhotecaUser
from library.models import Book, Author, Borrowing


def index(request):
    authors_count = Author.objects.all().filter(
        book__is_available=True).distinct().count()
    books_count = Book.objects.filter(is_available=True).count()
    form = CreateUserForm()
    loses = Borrowing.objects.filter(
        late=True,
        date_returned=None).count()
    context = {
        'form': form,
        'books_count': books_count,
        'authors_count': authors_count,
        'stats': {
            'borrows': Borrowing.objects.all().count(),
            'loses': loses,
            'users': MinhotecaUser.objects.all().count()
        }
    }
    return render(request, 'index.html', context)
