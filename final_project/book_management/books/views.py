from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.db import connection


def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

def book_report(request):
    genre = request.GET.get('genre', '')
    year_start = request.GET.get('year_start', '')
    year_end = request.GET.get('year_end', '')

    books = Book.objects.all()

    if genre:
        books = books.filter(genre__icontains=genre)
    
    if year_start and year_end:
        books = books.filter(year__gte=year_start, year__lte=year_end)
    elif year_start:
        books = books.filter(year__gte=year_start)
    elif year_end:
        books = books.filter(year__lte=year_end)

    total_books = books.count()
    oldest_year = books.order_by('year').first().year if books else None
    newest_year = books.order_by('-year').first().year if books else None

    context = {
        'books': books,
        'total_books': total_books,
        'oldest_year': oldest_year,
        'newest_year': newest_year,
        'genre': genre,
        'year_start': year_start,
        'year_end': year_end,
    }
    
    return render(request, 'books/book_report.html', context)



def get_books_by_year_range(start_year, end_year):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books WHERE year BETWEEN %s AND %s", [start_year, end_year])
        result = cursor.fetchall()
    return result
