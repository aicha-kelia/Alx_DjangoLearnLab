from django.db import models

# Author model: represents a book author
class Author(models.Model):
    # The author's name (string, max 100 characters)
    name = models.CharField(max_length=100)

    # __str__ method: makes it readable in admin and shell
    def __str__(self):
        return self.name


# Book model: represents a book written by an author
class Book(models.Model):
    # Book title (string, max 200 characters)
    title = models.CharField(max_length=200)
    # Year the book was published (integer)
    publication_year = models.IntegerField()
    # ForeignKey linking each book to one author (one-to-many relationship)
    # on_delete=models.CASCADE ensures books are deleted if author is deleted
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # __str__ method: makes it readable in admin and shell
    def __str__(self):
        return self.title
