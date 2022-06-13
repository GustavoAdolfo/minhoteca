from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Book


@login_required(login_url='/accounts/login/')
def index(request):
    books = Book.objects.all()
    return render(request, 'library.html', {'books': books})
