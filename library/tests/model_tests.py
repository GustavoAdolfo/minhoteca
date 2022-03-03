from django.test import TestCase
from library.models import Book, Author, Publisher


class AuthorModelTests(TestCase):

    def test_creat_author(self):
        author = Author.objects.create(
            name='John Doe',
            wikipedia='https://en.wikipedia.org/wiki/John_Doe',
            country='United States',
            picture_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Francis_Scott_Fitzgerald_1937_June_4_%281%29_%28photo_by_Carl_van_Vechten%29.jpg/800px-Francis_Scott_Fitzgerald_1937_June_4_%281%29_%28photo_by_Carl_van_Vechten%29.jpg'
        )
        author.full_clean()
        author.save()

        list_authors = Author.objects.all()
        self.assertEqual(len(list_authors), 1)
        self.assertTrue(list_authors[0].name, 'John Doe')


class PublisherModelTests(TestCase):

    def test_create_publisher(self):
        publisher = Publisher.objects.create(
            name='Scribner',
            website='https://www.simonandschusterpublishing.com/scribner/'
        )
        publisher.full_clean()
        publisher.save()

        list_publishers = Publisher.objects.all()
        self.assertEqual(len(list_publishers), 1)
        self.assertTrue(list_publishers[0].name, 'John Doe')


class BookModelTests(TestCase):

    def test_book_creation(self):
        author = Author.objects.create(
            name='F. Scott Fitzgerald',
            wikipedia='https://pt.wikipedia.org/wiki/F._Scott_Fitzgerald',
            country='United States',
        )
        author.full_clean()
        author.save()

        publisher = Publisher.objects.create(
            name='Scribner',
            website='https://www.simonandschusterpublishing.com/scribner/'
        )
        publisher.full_clean()
        publisher.save()

        book = Book.objects.create(
            title='The Great Gatsby',
            subtitle='A novel',
            synopsis='A novel about a',
            language='English',
            is_available=True,
            isbn=123456789
        )
        book.author_id = author
        book.publisher_id = publisher
        book.full_clean()
        book.save()
        list_of_books = Book.objects.all()
        self.assertEqual(len(list_of_books), 1)
        self.assertEqual(list_of_books[0].title, 'The Great Gatsby')
