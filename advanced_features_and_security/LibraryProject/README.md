# LibraryProject - Advanced Features and Security

## Permissions and Groups

### Models
- **Book model**
  - Custom permissions:
    - `can_view` → allows users to view book details
    - `can_create` → allows users to create new books
    - `can_edit` → allows users to edit existing books
    - `can_delete` → allows users to delete books

### Views
- `book_list` → lists all books (requires `can_view`)
- `view_book` → shows book details (requires `can_view`)
- `edit_book` → edits a book (requires `can_edit`)

### Groups
- **Editors** → can_edit, can_create
- **Viewers** → can_view
- **Admins** → can_view, can_create, can_edit, can_delete

### Notes
- Permissions are enforced with `@permission_required`.
- URLs are defined in `bookshelf/urls.py`.
- Only users with proper permissions can access each view.
