from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    wikipedia = models.URLField(blank=True, max_length=500)
    country = models.CharField(max_length=100, blank=True)
    picture_url = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'


class Book(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, blank=True)
    synopsis = models.TextField(blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.DO_NOTHING, default=0)
    publisher = models.ForeignKey(
        Publisher, default=0, on_delete=models.DO_NOTHING)
    language = models.CharField(max_length=20)
    is_available = models.BooleanField(default=False)
    isbn = models.IntegerField()
    picture_url = models.URLField(blank=True, max_length=500)

    def __str__(self):
        if self.subtitle:
            return '{} - {}'.format(self.title, self.subtitle)

        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
