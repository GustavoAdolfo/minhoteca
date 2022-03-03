from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, blank=True)
    synopsis = models.TextField(blank=True)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150)
    language = models.CharField(max_length=20)
    is_available = models.BooleanField(default=False)
    isbn = models.IntegerField()

    def __str__(self):
        if self.subtitle:
            return '{} - {}'.format(self.title, self.subtitle)

        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
