from rest_framework import serializers
from .models import Book, Author
import datetime

# Serializer for Book model: converts Book instances to JSON and validates input
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # serialize all fields of the Book model

    # Custom validation: ensures publication_year is not in the future
    def validate_publication_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Date of publication cannot be in the future.")
        return value


# Serializer for Author model: includes nested BookSerializer for related books
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer for related books
    # 'book_set' is the default reverse relation name from ForeignKey
    book_set = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'  # serialize all fields of the Author model
