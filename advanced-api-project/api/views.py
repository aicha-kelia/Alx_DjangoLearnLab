from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    BookListView API
    ----------------
    Features implemented:
    1. Filtering via DjangoFilterBackend: title, author, publication_year
    2. Searching via SearchFilter: title, author
    3. Ordering via OrderingFilter: title, publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Changed

    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Public: anyone can view a book detail
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Changed


class BookCreateView(generics.CreateAPIView):
    """
    Authenticated users only can create books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Changed


class BookUpdateView(generics.UpdateAPIView):
    """
    Authenticated users only can update books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Changed


class BookDeleteView(generics.DestroyAPIView):
    """
    Authenticated users only can delete books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Changed