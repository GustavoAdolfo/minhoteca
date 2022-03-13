import factory
from library.models import Author, Publisher, Book


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.sequence(lambda n: 'Author {}'.format(n))
    wikipedia = factory.sequence(
        lambda n: 'https://en.wikipedia.org/wiki/Author_{}'.format(n))
    country = factory.sequence(lambda n: 'Country {}'.format(n))
    picture_url = factory.sequence(
        lambda n: 'https://en.wikipedia.org/Author_{}.jpg'.format(n))


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.sequence(lambda n: 'Publisher {}'.format(n))
    website = factory.sequence(
        lambda n: 'https://en.wikipedia.org/wiki/Publisher_{}'.format(n))


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.sequence(lambda n: 'Book {}'.format(n))
    subtitle = factory.sequence(lambda n: 'Subtitle {}'.format(n))
    synopsis = factory.sequence(lambda n: 'Synopsis {}'.format(n))
    author = factory.SubFactory(AuthorFactory)
    publisher = factory.SubFactory(PublisherFactory)
    language = factory.sequence(lambda n: 'Language {}'.format(n))
    is_available = factory.sequence(lambda n: n % 2 == 0)
    isbn = factory.sequence(lambda n: n)
