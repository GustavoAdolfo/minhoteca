import operator
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Value  # , Q
from django.db.models.functions import Concat
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from .models import Book, Author


url = staticfiles_storage.path('countries.json')
countries = []
try:
    with open(url, "r", encoding='utf-8') as cdata:
        CONTENT = ''.join(cdata.readlines())
        countries = json.loads(CONTENT)
        countries = list(filter(lambda x: 'pt-br' in x, countries))
except Exception:
    pass


@login_required(login_url='/accounts/login/')
def index(request):
    """Retorna os livros cadastrados."""
    ord = request.GET.get('ord')
    if ord and ord == '2':
        books = Book.objects.order_by('-title').filter(is_available=True)
    elif ord and ord == '3':
        books = Book.objects.order_by('author__name').filter(is_available=True)
    elif ord and ord == '4':
        books = Book.objects.order_by('-author__name').filter(is_available=True)
    else:
        books = Book.objects.order_by('title').filter(is_available=True)
    paginator = Paginator(books, 20)
    pg = request.GET.get('pg')
    books = paginator.get_page(pg)
    classifications = [
        {'id': '1', 'description': 'Título de A - Z'},
        {'id': '2', 'description': 'Título de Z - A'},
        {'id': '3', 'description': 'Autor de A - Z'},
        {'id': '4', 'description': 'Autor de Z - A'}
    ]
    return render(request, 'library.html',
                  {'books': books, 'classifications': classifications})

def search_books(request):
    """Retorna o resultado de uma busca por livros."""
    try:
        expression = request.GET.get('term_search')
        if not expression:
            messages.add_message(
                request, messages.ERROR, 'Informe um valor para a busca.')
            return redirect('library:books')

        fields = Concat('title', Value(' '), 'subtitle',
                        Value(' '), 'author__name')
        books = Book.objects.annotate(
            title_subtitle=fields
        ).filter(
            title_subtitle__icontains=expression,
            is_available=True
        )
        if not books or len(books) == 0:
            messages.add_message(
                request, messages.WARNING,
                'Nenhum livro encontrado com o termo solicitado.')
            return redirect('library:books')

        ord = request.GET.get('ord')
        if ord and ord == '2':
            sorted_list = sorted(
                books, key=operator.attrgetter('title'), reverse=True)
        elif ord and ord == '3':
            sorted_list = sorted(
                books, key=operator.attrgetter('author.name'))
        elif ord and ord == '4':
            sorted_list = sorted(
                books, key=operator.attrgetter('author.name'), reverse=True)
        else:
            sorted_list = sorted(books, key=operator.attrgetter('title'))

        paginator = Paginator(sorted_list, 10)
        pg = request.GET.get('pg')
        books = paginator.get_page(pg)
        classifications = [
            {'id': '1', 'description': 'Título de A - Z'},
            {'id': '2', 'description': 'Título de Z - A'},
            {'id': '3', 'description': 'Autor de A - Z'},
            {'id': '4', 'description': 'Autor de Z - A'}
        ]
        return render(request, 'library.html',
                      {'books': books, 'classifications': classifications})
    except Book.DoesNotExist:
        raise Http404()

def book(request):
    pass

def author(request):
    pass