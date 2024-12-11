from django.db import models
from django.db import transaction

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.title

class Meta:
    indexes = [
        models.Index(fields=['genre']),
        models.Index(fields=['year']),
    ]

def update_books_year(books, new_year):
    with transaction.atomic():
        for book in books:
            book.year = new_year
            book.save()
