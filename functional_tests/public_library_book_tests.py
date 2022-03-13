import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_test import BaseTest
from selenium.webdriver.support.ui import Select
from library.models import Author, Publisher
from factories.library_factories import BookFactory


class LibraryTest(BaseTest):

    def test_can_show_public_books_home_page(self):
        # Um visitante do site resolve visitar a lista pública
        # de livros disponíveis.
        # =====================================================
        # A site visitor decides to consult the public list of
        # available books.
        self.webdriver.get(self.live_server_url + '/books/')
        # O visitante identifica um título na página onde se lê
        # "Livros Disponíveis".
        # ======================================================
        # The visitor identifies a title on the page where it reads
        # "Livros Disponíveis".
        title = self.webdriver.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(title.text, 'Livros Disponíveis')
        # Ele verifica também que há uma tabela com uma coluna entitulada
        # "Título" e uma coluna entitulada "Auutor".
        # ===============================================================
        # He verifies that there is a table with a column entitled "Título"
        # and another column entitled "Autor".
        table = self.webdriver.find_element(By.ID, 'table-book-list')
        table_headers = table.find_elements(By.TAG_NAME, 'th')
        self.assertEqual(len(table_headers), 2)
        self.assertTrue(
            any(header.text == 'Título' for header in table_headers),
            'No table header was found with the text "Título"')
        self.assertTrue(
            any(header.text == 'Autor' for header in table_headers),
            'No table header was found with the text "Autor"')

    def test_can_show_public_books_list(self):
        # Um visitante do site resolve visitar a lista pública
        # de livros disponíveis e verifica que são exibidos 10 livros
        # numa tabela contendo título e autor.
        # =====================================================
        # A site visitor decides to consult the public list of
        # available books and verifies that there are 10 books
        # displayed in a table with the title and author columns.
        BookFactory.create_batch(10)
        self.webdriver.get(self.live_server_url + '/books/')
        table = self.webdriver.find_element(By.ID, 'table-book-list')
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        self.assertTrue(len(tbody.find_elements(By.TAG_NAME, 'tr')) == 10)
        self.assertIn('Book 1', self.webdriver.page_source)
        self.assertIn('Author 1', self.webdriver.page_source)
