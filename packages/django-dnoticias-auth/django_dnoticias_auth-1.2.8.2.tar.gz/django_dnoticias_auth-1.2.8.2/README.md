=====
dnoticias_auth
=====

dnoticias_auth is a Django app to make the authentication in the DNOTICIAS PLATFORMS.

Quick start
-----------

1. Add "dnoticias_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dnoticias_auth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('auth/', include('dnoticias_auth.urls')),

3. Run ``python manage.py migrate`` to create the dnoticias_auth models.

4. Add the necessary settings variables

5. Add the following middleware:

```
MIDDLEWARE = [
    ...
    'dnoticias_auth.middleware.LoginMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'dnoticias_auth.middleware.TokenMiddleware',
]
```
LoginMiddleware is a preprocessor that will see the cookies and simulate an OIDC login action, this needs to be before mozilla SessionRefresh.

TokenMiddleware is a posprocessor that will take the session variables (if the user is logged in) and put them into cookies. This is used in another clients on the LoginMiddleware

## Settings variables

| Setting  | Default value | Description |
| ------------- | ------------- | ------------- |
| OIDC_STORE_ACCESS_TOKEN  | True | OIDC store access token in session (TRUE ONLY) |
| OIDC_STORE_ID_TOKEN  | True | OIDC store id token in session (TRUE ONLY) |
| AUTH_COOKIE_EXPIRATION_MINUTES  | 15 | Cookie expiration time |
| AUTH_COOKIE_DOMAIN  | dnoticias.pt | Cookie domain |
| AUTH_COOKIE_SECURE  | True | Secure cookie in HTTPS only |
| AUTH_COOKIE_HTTPONLY  | True | Prevents changes from JS |
