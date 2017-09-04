# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware

EMAIL_LENGTH = getattr(settings, 'EMAIL_LENGTH', 254)
USER_MODEL = getattr(settings, 'USER_MODEL', None) or \
             getattr(settings, 'AUTH_USER_MODEL', None) or \
             'auth.User'

class GoogleAuthUser(models.Model):
    user = models.ForeignKey(to=USER_MODEL, related_name='google_auth_user', on_delete=models.CASCADE)
    email = models.EmailField(max_length=EMAIL_LENGTH, unique=True)
    token_expiry = models.DateTimeField(null=True)
    access_token = models.CharField(max_length=254,null=True)
    refresh_token = models.CharField(max_length=254,null=True)

def get_users_by_email(email):
    return User.objects.filter(**{"email__iexact": email}) 

def create_user(name, last_name, email):
    return get_user_model().objects.update_or_create(
            email=email,
            defaults={"username": email,
                "first_name": name,
                "last_name": last_name})

def create_google_auth_user(user, email, access_token, refresh_token, token_expiry):
    return GoogleAuthUser.objects.update_or_create(
            user=user,
            email=email,
            defaults={"access_token": access_token,
                "refresh_token": refresh_token,
                "token_expiry": make_aware(token_expiry)})
