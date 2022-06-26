import operator
import json
import logging
import environ
from socketserver import DatagramRequestHandler
from django.utils.html import strip_tags
from django.core import mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Value  # , Q
from django.db.models.functions import Concat
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from .models import Book, Author, Borrowing
from .forms import BorrowingForm

env = environ.Env()
environ.Env.read_env()
log = logging.getLogger()
log.setLevel(logging.INFO)

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
    order = request.GET.get('ord')
    if order and order == '2':
        books = Book.objects.order_by('-title').filter(is_available=True)
    elif order and order == '3':
        books = Book.objects.order_by('author__name').filter(is_available=True)
    elif order and order == '4':
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

@login_required(login_url='/accounts/login/')
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

        order = request.GET.get('ord')
        if order and order == '2':
            sorted_list = sorted(
                books, key=operator.attrgetter('title'), reverse=True)
        elif order and order == '3':
            sorted_list = sorted(
                books, key=operator.attrgetter('author.name'))
        elif order and order == '4':
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

@login_required(login_url='/accounts/login/')
def book(request, id:int):
    """Retorna os dados livro solicitado."""
    try:
        book_item = Book.objects.get(id=id)
        if not book_item.is_available:
            raise Http404()
        return render(request, 'book.html',
                      {'book': book_item})
    except Book.DoesNotExist:
        raise Http404()

@login_required(login_url='/accounts/login/')
def author(request, id:int):
    author_item = get_object_or_404(Author, id=id)
    books = author_item.book_set.filter(author_id=id,
                                    is_available=True)
    dic_author = {'author': author_item}
    country = next(filter(
        lambda x: x['pt-br'] == author_item.country, countries), None)
    if country:
        flag = f'data:image/png;base64, {country["flag"]}'
        dic_author.update({'flag': flag})
    else:
        dic_author.update({'flag': ''})

    return render(request, 'author.html',
                  {'author': dic_author, 'books': books})

@login_required(login_url='/accounts/login/')
def authors(request):
    """Lista autores cadastrados."""
    order = request.GET.get('ord')
    authors_data = Author.objects.order_by(
        'name').filter(book__is_available=True)
    if order and order == '2':
        ordered_list = sorted(
            authors_data, key=operator.attrgetter('name'), reverse=True)
    elif order and order == '3':
        ordered_list = sorted(
            authors_data, key=operator.methodcaller('count_books'), reverse=True)
    elif order and order == '4':
        ordered_list = sorted(
            authors_data, key=operator.methodcaller('count_books'))
    else:
        ordered_list = sorted(authors_data, key=operator.attrgetter('name'))

    authors_list = []
    for author_item in ordered_list:
        dic_autor = {'author': author_item}
        country = next(filter(
            lambda x: x['pt-br'] == author_item.country, countries), None)
        if country:
            flag = f'data:image/png;base64, {country["flag"]}'
            dic_autor.update({'flag': flag})
        else:
            dic_autor.update({'flag': ''})
        authors_list.append(dic_autor)
    paginator = Paginator(authors_list, 20)
    pg = request.GET.get('pg')
    authors_data = paginator.get_page(pg)
    classifications = [
        {'id': '1', 'description': 'Nome de A - Z'},
        {'id': '2', 'description': 'Nome de Z - A'},
        {'id': '3', 'description': 'Mais livros'},
        {'id': '4', 'description': 'Menos livros'}
    ]
    return render(request, 'authors.html',
                  {'authors': authors_data, 'classifications': classifications})

@login_required(login_url='/accounts/login/')
def search_authors(request):
    """Retorna o resultado de uma busca por autores."""
    try:
        expression = request.GET.get('term_search')
        if not expression:
            messages.add_message(
                request, messages.ERROR, 'Informe um valor para a busca.')
            return redirect('library:authors')

        fields = Concat('name', Value(' '), 'country')
        authors_data = Author.objects.order_by(
            'name').annotate(
                author_country=fields).filter(
            author_country__icontains=expression,
            book__is_available=True
        )
        if not authors_data or not len(authors_data):
            messages.add_message(
                request, messages.WARNING,
                'Nenhum autor encontrado com o termo solicitado.')
            return redirect('library:authors')

        order = request.GET.get('ord')
        if order and order == '2':
            ordered_list = sorted(
                authors_data, key=operator.attrgetter('name'), reverse=True)
        elif order and order == '3':
            ordered_list = sorted(
                authors_data, key=operator.methodcaller('count_books'),
                reverse=True)
        elif order and order == '4':
            ordered_list = sorted(
                authors_data, key=operator.methodcaller('count_books'))
        else:
            ordered_list = sorted(authors_data, key=operator.attrgetter('name'))

        authors_list = []
        for author_item in ordered_list:
            dic_autor = {'author': author_item}
            country = next(filter(
                lambda x: x['pt-br'] == author_item.country, countries), None)
            if country:
                flag = f'data:image/png;base64, {country["flag"]}'
                dic_autor.update({'flag': flag})
            else:
                dic_autor.update({'flag': ''})
            authors_list.append(dic_autor)
        paginator = Paginator(authors_list, 20)
        pg = request.GET.get('pg')
        authors_data = paginator.get_page(pg)
        classifications = [
            {'id': '1', 'description': 'Nome de A - Z'},
            {'id': '2', 'description': 'Nome de Z - A'},
            {'id': '3', 'description': 'Mais livros'},
            {'id': '4', 'description': 'Menos livros'}
        ]
        return render(request, 'authors.html',
                      {'authors': authors_data, 'classifications': classifications})
    except Author.DoesNotExist:
        raise Http404()

def _request_borrowing(request):
    borrower = request.user
    borrowed = Borrowing.objects.filter(
        borrower=borrower,date_returned=None).first()
    if borrowed:
        return render(request, 'borrow.html', {'borrowed': borrowed})

    if not book_id:
        messages.add_message(
            request, messages.WARNING, 'Informe um livro para empréstimo.')
        return redirect('library:index')

    book_id = request.GET.get('book')
    selected_book = Book.objects.filter(id=book_id).first()
    if selected_book.is_available:
        form = BorrowingForm()
        form.initial['book_id'] = selected_book.id
        form.initial['borrower_id'] = borrower.id
        context = {
            'book_title': selected_book.title,
            'form': form
            }
        return render(request, 'borrow.html', {'context': context})
    
    messages.add_message(
        request, messages.WARNING, 'O livro selecionado não está disponível.')
    return redirect('library:index')


def _save_borrowing(request):
    form = BorrowingForm(request.POST)
    try:
        if form.is_valid():
            new_borrow = form.save()
            borrower = request.user
            if new_borrow:
                current_site = get_current_site(request)
                subject = 'Você solicitou um livro emprestado na Minhoteca'
                to_email = getattr(borrower, 'email')
                message = render_to_string(
                    'emails/account_activation_email.html',
                    {
                        'user': borrower,
                        'domain': current_site.domain,
                        'uid': '12345',
                        'token': '12345'
                    })
                plain_message=strip_tags(message)
                mail.send_mail(subject, plain_message,
                    from_email=env('DEFAULT_FROM_EMAIL'),
                    recipient_list=[to_email], html_message=message)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Sua solicitação foi registrada e uma confirmação enviada '
                    'para o seu e-mail. No dia e hora marcados, compareça à '
                    'estação Tamanduateí do Metrô de São Paulo para pegar o '
                    'livro',
                    extra_tags='safe')
                return HttpResponseRedirect('/')
        
        selected_book = Book.objects.filter(
            id=form.cleaned_data['book_id']).first()
        context = {
            'book_title': selected_book.title,
            'form': form
            }
        return render(request, 'borrow.html', {'context': context})
    except Exception as error:
        log.error(error)
        messages.warning(
            request,
            ('Ocorreu uma falha ao realizar a solicitação. '+
            'Por favor tente novamente mais tarde.')
        )
        return HttpResponseRedirect('/')

@login_required(login_url='/accounts/login/')
def borrow(request):
    """Retorna o formulário de empréstimo ou o livro atualmente emprestado."""
    if request.method == 'POST':
        return _save_borrowing(request)
    
    return _request_borrowing(request)
    

def borrowers(request):
    pass