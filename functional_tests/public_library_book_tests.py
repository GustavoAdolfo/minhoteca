import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_test import BaseTest
from selenium.webdriver.support.ui import Select
from library.models import Author, Publisher


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
