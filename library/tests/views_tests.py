from django.urls import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from library.views import index
from factories import library_factories


class LibraryViewsTests(TestCase):

    def test_url_resolves_to_books_index_view(self):
        found = resolve('/books/')
        self.assertEqual(found.func, index)

    def test_index_view_return_correct_html(self):
        response = self.client.get('/books/')
        self.assertTemplateUsed(response, 'library_index.html')

        html = response.content.decode('utf8')
        expected_content = render_to_string('library_index.html')
        self.assertEqual(html, expected_content)

    def test_book_homepage_returns_books(self):
        library_factories.BookFactory.create_batch(10)
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 10)
        self.assertIn('Book 1', response.content.decode('utf8'))
