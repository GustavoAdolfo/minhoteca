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


url = staticfiles_storage.path('data/countries.json')
countries = []
try:
    with open(url, "r", encoding='utf-8') as cdata:
        CONTENT = ''.join(cdata.readlines())
        countries = json.loads(CONTENT)
        countries = list(filter(lambda x: 'pt-br' in x, countries))
except Exception as ex:
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

def book(request, id:int):
    """Retorna os dados livro solicitado."""
    try:
        book = Book.objects.get(id=id)
        if not book.is_available:
            raise Http404()
        return render(request, 'book.html',
                      {'book': book})
    except book.DoesNotExist:
        raise Http404()

def author(request, id:int):
    author = get_object_or_404(Author, id=id)
    books = author.book_set.filter(author_id=id,
                                    is_available=True)
    dic_author = {'author': author}
    country = next(filter(
        lambda x: x['pt-br'] == author.country, countries), None)
    if country:
        dic_author.update(
            {'flag': 'data:image/png;base64, {0}'.format(country['flag'])})
    else:
        dic_author.update({'flag': ''})

    return render(request, 'author.html',
                  {'author': dic_author, 'books': books})

def authors(request):
    """Lista autores cadastrados."""
    ord = request.GET.get('ord')
    authors = Author.objects.order_by(
        'name').filter(book__is_available=True).distinct()
    if ord and ord == '2':
        ordered_list = sorted(
            authors, key=operator.attrgetter('name'), reverse=True)
    elif ord and ord == '3':
        ordered_list = sorted(
            authors, key=operator.methodcaller('count_books'), reverse=True)
    elif ord and ord == '4':
        ordered_list = sorted(
            authors, key=operator.methodcaller('count_books'))
    else:
        ordered_list = sorted(authors, key=operator.attrgetter('name'))

    authors_list = []
    for author in ordered_list:
        dic_autor = {'author': author}
        country = next(filter(
            lambda x: x['pt-br'] == author.country, countries), None)
        if country:
            dic_autor.update(
                {'flag': 'data:image/png;base64, {0}'.format(country['flag'])})
        else:
            dic_autor.update({'flag': ''})
        authors_list.append(dic_autor)
    paginator = Paginator(authors_list, 20)
    pg = request.GET.get('pg')
    authors = paginator.get_page(pg)
    classifications = [
        {'id': '1', 'description': 'Nome de A - Z'},
        {'id': '2', 'description': 'Nome de Z - A'},
        {'id': '3', 'description': 'Mais livros'},
        {'id': '4', 'description': 'Menos livros'}
    ]
    return render(request, 'authors.html',
                  {'authors': authors, 'classification': classifications})
