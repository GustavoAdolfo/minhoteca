from datetime import datetime
from django.db import models
from accounts.models import MinhotecaUser


class Author(models.Model):
    name = models.CharField(max_length=100)
    wikipedia = models.URLField(blank=True, max_length=500)
    country = models.CharField(max_length=100, blank=True)
    picture_url = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return str(self.name)
    
    def count_books(self):
        return self.book_set.filter(is_available=True).count()

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'


class Book(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.DO_NOTHING, default=0)
    publisher = models.ForeignKey(
        Publisher, default=0, on_delete=models.DO_NOTHING)
    language = models.CharField(max_length=20)
    is_available = models.BooleanField(default=0)
    isbn = models.PositiveBigIntegerField()
    # isbn = models.CharField(max_length=13, blank=False)
    picture_url = models.URLField(blank=True, max_length=500)
    borrowed = models.BooleanField(default=False)

    def __str__(self):
        if self.subtitle:
            return f'{self.title} - {self.subtitle}'

        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    borrower = models.ForeignKey(MinhotecaUser, on_delete=models.DO_NOTHING)
    date_borrowed = models.DateField(blank=True, null=True)
    date_returned = models.DateField(blank=True, null=True)
    date_requested = models.DateField(auto_now_add=True)
    late = models.BooleanField(default=False)
    schedule = models.TimeField(blank=False, null=False)
    return_forecast = models.DateField(blank=False, null=False)

    def status(self):
        if self.date_returned and self.date_returned <= self.return_forecast:
            return 'Devolvido antes do prazo'
        elif self.date_returned and self.date_requested == self.return_forecast:
            return 'Devolvido no prazo'
        elif self.date_returned and self.date_returned > self.return_forecast:
            self.late = True
            self.save()
            return 'Devolvido com atraso'
        elif not self.date_returned and self.return_forecast < datetime.now().date():
            self.late = True
            self.save()
            return 'Em atraso'
        else:
            return 'Aguardando devolução'

    def css_status(self):
        if self.date_returned and self.date_returned <= self.return_forecast:
            return 'bg-success'
        elif self.date_returned and self.date_requested == self.return_forecast:
            return 'bg-info'
        elif self.date_returned and self.date_returned > self.return_forecast:
            return 'bg-warning'
        elif not self.date_returned and self.return_forecast < datetime.now().date():
            return 'bg-danger'
        else:
            return ''

    class Meta:
        verbose_name = 'Borrowing'
        verbose_name_plural = 'Borrowings'