from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def form_example(request):
    form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})