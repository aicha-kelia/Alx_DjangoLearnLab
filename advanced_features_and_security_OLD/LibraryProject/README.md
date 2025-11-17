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

## Task 3 – HTTPS & Secure Redirects

- SECURE_SSL_REDIRECT = True
- SESSION_COOKIE_SECURE / CSRF_COOKIE_SECURE = True
- HSTS configured:
  - SECURE_HSTS_SECONDS = 31536000 (1 year)
  - SECURE_HSTS_INCLUDE_SUBDOMAINS = True
  - SECURE_HSTS_PRELOAD = True
- X_FRAME_OPTIONS = DENY
- SECURE_CONTENT_TYPE_NOSNIFF / SECURE_BROWSER_XSS_FILTER = True
- Content Security Policy applied (CSP_DEFAULT_SRC, CSP_SCRIPT_SRC, CSP_STYLE_SRC, etc.)
- Tested: HTTP requests redirect to HTTPS (ready for production)
