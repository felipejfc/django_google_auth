# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions, authentication, HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .models import get_users_by_email

class GoogleAuthBackend(object):
    """
    Authenticate all requests against google, so that when the access token is revoked, the user will lose access immediately.

    Pass the access token in the header of the request, like:

    Authentication: token TOKEN
    """

    def authenticate(self, request, token=None):
        return None

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
        auth_header = get_authorization_header(request).decode(HTTP_HEADER_ENCODING)
        auth = auth_header.split()
        if not auth or auth[0].lower() != 'token':
            return None

        if len(auth)!=2:
            msg = 'Invalid authorization header.'
            raise exceptions.AuthenticationFailed(msg)
        token = auth[1]
        r = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(token))
        if r.status_code != 200:
            return None
        acc_info = r.json()
        email = acc_info['email']
        user = get_users_by_email(email)
        if len(user) <= 0:
            return None
        else:
            return user[0], token
