from django.shortcuts import render
from .models import Book


def index(request):
    books = Book.objects.all()
    return render(request, 'library_index.html', {'books': books})
