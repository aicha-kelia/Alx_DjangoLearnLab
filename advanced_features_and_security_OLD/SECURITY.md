# Task 3 – HTTPS & Secure Redirects

- SECURE_SSL_REDIRECT = True
- SESSION_COOKIE_SECURE / CSRF_COOKIE_SECURE = True
- HSTS configured (1 year, include subdomains, preload)
- X_FRAME_OPTIONS = DENY
- SECURE_CONTENT_TYPE_NOSNIFF / SECURE_BROWSER_XSS_FILTER = True
- Content Security Policy applied
- Tested: HTTP requests redirect to HTTPS (ready for production)
