# Book model custom permissions:
# can_view   -> allows users to view book details
# can_create -> allows users to create new books
# can_edit   -> allows users to edit existing books
# can_delete -> allows users to delete books
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title
