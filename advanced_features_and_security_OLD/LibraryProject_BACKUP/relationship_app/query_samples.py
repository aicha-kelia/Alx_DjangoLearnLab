from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None

def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None

def retrieve_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except:
        return None