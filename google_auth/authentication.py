# -*- coding: utf-8 -*-

import requests
import httplib2
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from rest_framework import exceptions, authentication, HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .models import get_users_by_email, get_google_auth_user_by_app_token

token_verification_url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
refresh_token_url = 'https://www.googleapis.com/oauth2/v4/token'
client_id = getattr(settings, 'GOOGLE_AUTH_CLIENT_ID', '')
client_secret = getattr(settings, 'GOOGLE_AUTH_CLIENT_SECRET', '')

class GoogleAuthBackend(object):
    """
    Authenticate all requests against google, so that when the access token is revoked, the user will lose access immediately.

    Pass the access token in the header of the request, like:

    Authentication: token TOKEN
    """

    def authenticate(self, request, token=None):
        user, _ = do_authentication(token)
        return user

    def get_user(self, user_id):
        try:
            return get_user_model.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class GoogleAuthAuthentication(BaseAuthentication):
    """
    Returns two-tuple of (user, token) if authentication succeeds,
    or None otherwise.
    """
    def authenticate(self, request):
        app_token = get_token_from_request_header(request)
        return do_authentication(app_token)

def do_authentication(app_token=None):
    google_auth_user = get_google_auth_user_by_app_token(app_token)
    if not google_auth_user:
        return None
    if google_auth_user.token_expiry < make_aware(datetime.now()):
        google_auth_user = refresh_access_token(google_auth_user)
    r = requests.get(token_verification_url.format(google_auth_user.access_token))
    if r.status_code != 200:
        return None
    acc_info = r.json()
    email = acc_info.get('email','')
    user = get_users_by_email(email)
    return user, app_token

def get_token_from_request_header(request):
    auth_header = get_authorization_header(request).decode(HTTP_HEADER_ENCODING)
    auth = auth_header.split()
    if not auth or auth[0].lower() != 'token':
        return None
    if len(auth)!=2:
        msg = 'Invalid authorization header.'
        raise exceptions.AuthenticationFailed(msg)
    app_token = auth[1]
    return app_token

def refresh_access_token(google_auth_user):
    r = requests.post(refresh_token_url, data = {'client_id':client_id,
        'client_secret':client_secret,
        'refresh_token':google_auth_user.refresh_token,
        'grant_type':'refresh_token'})
    if r.status_code != 200:
        raise Exception('user google auth token is expired and unnable to be refreshed')
    res = r.json()
    google_auth_user.access_token = res.get('access_token','')
    google_auth_user.token_expiry = make_aware(
            datetime.now() + timedelta(seconds=
                res.get('expires_in',0) - 10
                ))
    google_auth_user.save()
    return google_auth_user

