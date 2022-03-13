from django.http import Http404
from django.shortcuts import render
from django.urls import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from library.views import index


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
