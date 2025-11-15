from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render
from .models import Book

# Only users with can_view permission can access this view
@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# Only users with can_edit permission can access this view
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # your edit logic here
    return render(request, 'bookshelf/book_edit.html', {'book': book})
