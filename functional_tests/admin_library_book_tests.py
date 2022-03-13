import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_test import BaseTest
from selenium.webdriver.support.ui import Select
from library.models import Author, Publisher


class LibraryTest(BaseTest):

    def test_admin_can_view_books_in_admin_page(self):
        # O administrador acessa a área administrativa e verifica que há uma
        # link para a tabela library
        # =====================================================================
        # The administrator accesses the administrative area and checks that
        # there is a link to the library table
        self.login_as_superuser()
        time.sleep(1)
        div_library = self.webdriver.find_element(By.CLASS_NAME, 'app-library')
        th_library = div_library.find_elements(By.TAG_NAME, 'th')
        self.assertIn('Books', [th.text for th in th_library])
        add_link = div_library.find_element(
            By.XPATH, '// a[@href="/admin/library/book/add/"]')
        self.assertIn('Add', add_link.text)

    def test_admin_can_access_add_new_book_form(self):
        self.login_as_superuser()
        # O administrador clica no link "Books" e é exibida uma tela contendo
        # uma lista vazia de livros
        # =====================================================================
        # The admin clicks the "Books" link and a screen is displayed
        # containing an empty list of books
        time.sleep(1)
        div_books = self.webdriver.find_element(By.CLASS_NAME, 'app-library')
        link_books = div_books.find_element(By.LINK_TEXT, 'Books')
        time.sleep(1)
        self.assertTrue(link_books.is_displayed())
        link_books.click()
        book_page = self.webdriver.current_url
        self.assertIn('/library/book', book_page)
        # O administrador verifica que há um botão onde se lê "add book +"
        # The admin checks that there is a button that reads "add book +"
        add_link = self.webdriver.find_element(
            By.XPATH, '// a[@href="/admin/library/book/add/"]')
        time.sleep(1)
        self.assertTrue(add_link.is_displayed())
        # O administrador clica no link e uma tela com um formulário de
        # cadastro é exibida
        # =====================================================================
        # The administrator clicks on the link and a screen with a registration
        # form is displayed
        add_link.click()
        form_book = self.webdriver.find_element(By.ID, 'book_form')
        self.assertTrue(form_book.is_displayed())
        page_titles = self.webdriver.find_elements(By.TAG_NAME, 'h1')
        self.assertIn('Add Book', [title.text for title in page_titles])

    def test_admin_checks_appropriate_fields_on_the_form(self):
        self.login_as_superuser()
        time.sleep(1)
        div_library = self.webdriver.find_element(By.CLASS_NAME, 'app-library')
        link_books = div_library.find_element(By.LINK_TEXT, 'Books')
        link_books.click()
        time.sleep(1)
        add_link = self.webdriver.find_element(
            By.XPATH, '// a[@href="/admin/library/book/add/"]')
        add_link.click()
        # O administrador verifica que os todos os campos para cadastro
        # de um livro estão presentes
        # =====================================================================
        # The administrator checks that all the fields for book registration
        # are present
        # - title
        input_title = self.webdriver.find_element(By.ID, 'id_title')
        self.assertTrue(input_title.is_displayed())
        # - subtitle
        input_subtitle = self.webdriver.find_element(By.ID, 'id_subtitle')
        self.assertTrue(input_subtitle.is_displayed())
        # - synopsis
        input_synopsis = self.webdriver.find_element(By.ID, 'id_synopsis')
        self.assertTrue(input_synopsis.is_displayed())
        # - author
        input_author = self.webdriver.find_element(By.ID, 'id_author')
        self.assertTrue(input_author.is_displayed())
        # - publish
        input_publisher = self.webdriver.find_element(By.ID, 'id_publisher')
        self.assertTrue(input_publisher.is_displayed())
        # - language
        input_language = self.webdriver.find_element(By.ID, 'id_language')
        self.assertTrue(input_language.is_displayed())
        # - is_available
        input_is_available = self.webdriver.find_element(
            By.ID, 'id_is_available')
        self.assertTrue(input_is_available.is_displayed())
        # - isbn
        input_isbn = self.webdriver.find_element(By.ID, 'id_isbn')
        self.assertTrue(input_isbn.is_displayed())

    def test_admin_can_add_a_book(self):
        self.login_as_superuser()

        author = Author.objects.create(
            name='John Doe',
            wikipedia='https://en.wikipedia.org/wiki/John_Doe',
            country='United States'
        )
        author.full_clean()
        author.save()

        publisher = Publisher.objects.create(
            name='Scribner',
            website='https://www.simonandschusterpublishing.com/scribner/'
        )
        publisher.full_clean()
        publisher.save()

        time.sleep(1)
        link_books = self.webdriver.find_element(By.LINK_TEXT, 'Books')
        link_books.click()
        time.sleep(1)
        add_link = self.webdriver.find_element(
            By.XPATH, '// a[@href="/admin/library/book/add/"]')
        add_link.click()
        time.sleep(1)
        # O administrador preenche todos os campos do formulário e clica em
        # "salvar"
        # =====================================================================
        # The admin fills all the form fields and clicks "save"
        # - title
        input_title = self.webdriver.find_element(By.ID, 'id_title')
        input_title.send_keys('Test Book')
        # - subtitle
        input_subtitle = self.webdriver.find_element(By.ID, 'id_subtitle')
        input_subtitle.send_keys('Test Subtitle')
        # - synopsis
        input_synopsis = self.webdriver.find_element(By.ID, 'id_synopsis')
        input_synopsis.send_keys('Test Synopsis')
        # - author
        select_author = Select(self.webdriver.find_element(
            By.ID, 'id_author'))
        select_author.select_by_visible_text('John Doe')
        # - publish
        select_publisher = Select(self.webdriver.find_element(
            By.ID, 'id_publisher'))
        select_publisher.select_by_visible_text('Scribner')
        # - language
        input_language = self.webdriver.find_element(By.ID, 'id_language')
        input_language.send_keys('Test Language')
        # - is_available
        input_is_available = self.webdriver.find_element(
            By.ID, 'id_is_available')
        input_is_available.click()
        # - isbn
        input_isbn = self.webdriver.find_element(By.ID, 'id_isbn')
        input_isbn.send_keys('9788594541222')
        # - save
        button_save = self.webdriver.find_element(By.NAME, '_save')
        button_save.click()
        # O sistema volta para a tela de listagem dos livros e o administrador
        # verifica que uma tabela listando os títulos, subtítulos, isbn e
        # disponibilidade dos livros aparece na tela.
        # =====================================================================
        # The system returns to the book listing screen and the administrator
        # verifies that a table listing the titles, subtitles, isbn and
        # availability of the books appears on the screen.
        time.sleep(1)
        table_books = self.webdriver.find_element(By.ID, 'result_list')
        self.assertTrue(table_books.is_displayed())
        item = table_books.find_elements(By.TAG_NAME, 'th')
        self.assertIn('Test Book', [book.text for book in item])

    def test_admin_try_add_a_new_book_without_filling_all_the_fields(self):
        # O administrador clica em adicionar um novo livro e o formulário
        # é novamente exibido
        # =====================================================================
        # The admin clicks add a new book and the form is redisplayed
        self.login_as_superuser()
        time.sleep(1)
        link_books = self.webdriver.find_element(By.LINK_TEXT, 'Books')
        link_books.click()
        time.sleep(1)
        add_link = self.webdriver.find_element(
            By.XPATH, '// a[@href="/admin/library/book/add/"]')
        add_link.click()
        time.sleep(1)
        form_book = self.webdriver.find_element(By.ID, 'book_form')
        self.assertTrue(form_book.is_displayed())
        # O administrador preenche os campos título, subtítulo e isbn e tecla
        # em enter
        # The administrator fills in the title, subtitle and isbn fields and
        # press enter key
        # - title
        input_title = self.webdriver.find_element(By.ID, 'id_title')
        input_title.send_keys('Second Book')
        # - subtitle
        input_subtitle = self.webdriver.find_element(By.ID, 'id_subtitle')
        input_subtitle.send_keys('Second Subtitle')
        # - isbn
        input_isbn = self.webdriver.find_element(By.ID, 'id_isbn')
        input_isbn.send_keys('9788594541333')
        input_isbn.send_keys(Keys.ENTER)
        time.sleep(1)
        # então o sistema acusa um erro alertando que alguns campos não foram
        # preenchidos
        # =====================================================================
        # then the system accuses an error warning that some fields were not
        # filled
        error_notes = self.webdriver.find_elements(By.CLASS_NAME, 'errornote')
        self.assertIn('Please correct the errors below.', [
                      error.text for error in error_notes])
        error_list = self.webdriver.find_element(By.CLASS_NAME, 'errorlist')
        errors = error_list.find_elements(By.TAG_NAME, 'li')
        self.assertIn('This field is required.',
                      [error.text for error in errors])

    def test_admin_try_add_a_new_book_with_incomplete_data(self):
        # O administrador clica em adcionar mais um livro e o formulário é
        # exibido
        # =====================================================================
        # The admin clicks add one more book and the form is displayed
        self.login_as_superuser()
        time.sleep(1)

        author = Author.objects.create(
            name='John Doe',
            wikipedia='https://en.wikipedia.org/wiki/John_Doe',
            country='United States'
        )
        author.full_clean()
        author.save()

        publisher = Publisher.objects.create(
            name='Scribner',
            website='https://www.simonandschusterpublishing.com/scribner/'
        )
        publisher.full_clean()
        publisher.save()

        link_books = self.webdriver.find_element(By.LINK_TEXT, 'Books')
        link_books.click()
        time.sleep(1)
        add_link = self.webdriver.find_element(
            By.XPATH, '// a[@href="/admin/library/book/add/"]')
        add_link.click()
        time.sleep(1)
        form_book = self.webdriver.find_element(By.ID, 'book_form')
        self.assertTrue(form_book.is_displayed())
        # O administrador, preenche título, author e publisher e tecla enter
        # =====================================================================
        # The administrator, fill in title, author and publisher e tecla enter
        # - title
        input_title = self.webdriver.find_element(By.ID, 'id_title')
        input_title.send_keys('New Book')
        # - author
        select_author = Select(
            self.webdriver.find_element(By.ID, 'id_author'))
        select_author.select_by_visible_text('John Doe')
        # - publisher
        select_publisher = Select(self.webdriver.find_element(
            By.ID, 'id_publisher'))
        select_publisher.select_by_visible_text('Scribner')
        # - save
        button_save = self.webdriver.find_element(By.NAME, '_save')
        button_save.click()
        # então o sistema acusa um erro alertando que alguns campos não foram
        # preenchidos
        # =====================================================================
        # then the system accuses an error warning that some fields were not
        # filled
        time.sleep(1)
        error_notes = self.webdriver.find_elements(By.CLASS_NAME, 'errornote')
        self.assertIn('Please correct the errors below.', [
                      error.text for error in error_notes])
        error_list = self.webdriver.find_element(By.CLASS_NAME, 'errorlist')
        errors = error_list.find_elements(By.TAG_NAME, 'li')
        self.assertIn('This field is required.',
                      [error.text for error in errors])

    def test_admin_edit_item_in_book_list(self):
        # O administrador verifica que alguns livros não estão marcados como
        # disponíveis
        # =====================================================================
        # The admin checks that some books are not marked as available
        self.login_as_superuser()
        time.sleep(1)
        div_books = self.webdriver.find_element(By.CLASS_NAME, 'app-library')
        link_books = div_books.find_element(By.LINK_TEXT, 'Books')
        link_books.click()
        time.sleep(1)
        add_link = self.webdriver.find_element(
            By.XPATH, '// a[@href="/admin/library/book/add/"]')
        add_link.click()
        # - title
        input_title = self.webdriver.find_element(By.ID, 'id_title')
        input_title.send_keys('Test Book')
        # - subtitle
        input_subtitle = self.webdriver.find_element(By.ID, 'id_subtitle')
        input_subtitle.send_keys('Test Subtitle')
        # - synopsis
        input_synopsis = self.webdriver.find_element(By.ID, 'id_synopsis')
        input_synopsis.send_keys('Test Synopsis')
        # - author
        input_author = self.webdriver.find_element(By.ID, 'id_author')
        input_author.send_keys('Test Author')
        # - publish
        input_publisher = self.webdriver.find_element(By.ID, 'id_publisher')
        input_publisher.send_keys('Test Publisher')
        # - language
        input_language = self.webdriver.find_element(By.ID, 'id_language')
        input_language.send_keys('Test Language')
        # - isbn
        input_isbn = self.webdriver.find_element(By.ID, 'id_isbn')
        input_isbn.send_keys('9788594541222')
        # - save
        button_save = self.webdriver.find_element(By.NAME, '_save')
        button_save.click()
        time.sleep(1)
        td_is_available = self.webdriver.find_elements(
            By.CLASS_NAME, 'field-is_available')
        self.assertEqual(len(td_is_available), 1)
        # O administrador clica na caixa de seleção para definir que um livro
        # está disponível e clica em salvar
        # =====================================================================
        # The admin clicks the checkbox to define a book is available and
        # clicks save
        input_is_available = td_is_available[0].find_element(
            By.TAG_NAME, 'input')
        input_is_available.click()
        button_save = self.webdriver.find_element(By.NAME, '_save')
        button_save.click()
        time.sleep(1)
        # O administrador agora verifica que o livro está marcado como
        # disponílvel
        # =====================================================================
        # The admin now verifies that the book is checked as available
        td_is_available = self.webdriver.find_elements(
            By.CLASS_NAME, 'field-is_available')
        input_is_available = td_is_available[0].find_element(
            By.TAG_NAME, 'input')
        self.assertTrue(input_is_available.is_selected())
