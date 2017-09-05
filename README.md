django-google-auth
==================

A google auth authenticator backend for django and django rest framework.
This backend will always validate all requests against google, so that when a user has it's email removed from the domain, it will lose access.

### Installation
```
pip install django-google-auth
```

Add google_auth to your INSTALLED_APPS
```
INSTALLED_APPS = (
    ...
    'google_auth',
)
```

Include auth urls to your urls.py
```
urlpatterns = patterns(
    ...
    (r'^google_auth/', include('google_auth.urls')),
)
```

Include google_auth.authentication.GoogleAuthBackend to AUTHENTICATION_BACKENDS
```
AUTHENTICATION_BACKENDS = (
    ...
    "google_auth.authentication.GoogleAuthBackend",
)
```

### Settings
The settings of this app are:
- GOOGLE_AUTH_CLIENT_ID
the client id of your google app
- GOOGLE_AUTH_CLIENT_SECRET
the client secret of your google app
- GOOGLE_AUTH_AUTHORIZED_DOMAINS
the email domains that are authorized to use your app (defaults to gmail.com)
- GOOGLE_AUTH_SCOPE
the scope of the authorization (defaults to "email profile")
- GOOGLE_AUTH_REDIRECT_URL
the redirect url after google authorization, must change it to some endpoint that contains some business logic of yours (defaults to "localhost:8000")

all of them must be set.

### Flow to get authentication and refresh token
e.g. (assuming that urls are mounted as in the example above)
```
$ curl localhost:8000/auth/code_url
https://accounts.google.com/o/oauth2/v2/auth?client_id=xxxx&redirect_uri=http%3A%2F%2Fwww.127.0.0.1.xip.io%3A8000%2Fauth%2Fcomplete%2F&scope=email+profile&access_type=offline&response_type=code
```
User access the url from a browser and complete the login @ google, GOOGLE_AUTH_REDIRECT_URL will be called, containing the code:
e.g.
```
GOOGLE_AUTH_REDIRECT_URL/?code=xxxxxxxxx#
```
Code should then be exchanged by an access token and refresh token (this will also create a Django User)
```
curl -X POST "localhost:5000/google_auth/authenticate/?code=xxxxxxxxx"
{"access_token": "ya29.xxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxx-xxxxxxxxxxxxxxx", "refresh_token": xxxxxxxxxxxxx, "token_expiry": "2017-09-05T21:46:33.809210", "email": "me@felipejfc.com"}
```

### Authenticating requests
After completing the above flow, to authenticate an user's request, set an Authorization header
```
Authorization: token ya29.xxxxxxxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

##### Rest Framework
For django rest framework, add google_auth.authentication.GoogleAuthAuthentication to REST_FRAMEWORK.DEFAULT_AUTHENTICATOR_CLASSES
```
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        google_auth.authentication.GoogleAuthAuthentication,
    ),
```
