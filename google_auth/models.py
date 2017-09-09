# -*- coding: utf-8 -*-

import uuid
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
    app_token = models.CharField(max_length=254, blank=True, unique=True, default=uuid.uuid4)
    token_expiry = models.DateTimeField(null=True)
    access_token = models.CharField(max_length=254,null=True)
    refresh_token = models.CharField(max_length=254,null=True)

def regenerate_app_token(app_token):
    new_token = uuid.uuid4()
    GoogleAuthUser.objects.filter(app_token=app_token).update(app_token=new_token)
    return new_token

def get_google_auth_user_by_app_token(app_token):
    return GoogleAuthUser.objects.filter(**{"app_token": app_token}).first()

def get_google_auth_user_by_email(email):
    return GoogleAuthUser.objects.filter(**{"email__iexact": email}).first()

def get_users_by_email(email):
    return User.objects.filter(**{"email__iexact": email}).first()

def create_user(name, last_name, email):
    username=email.split("@")[0]
    return get_user_model().objects.update_or_create(
            email=email,
            defaults={"username": username,
                "first_name": name,
                "last_name": last_name})

def create_google_auth_user(user, email, access_token, refresh_token, token_expiry):
    return GoogleAuthUser.objects.update_or_create(
            user=user,
            email=email,
            defaults={"access_token": access_token,
                "refresh_token": refresh_token,
                "token_expiry": make_aware(token_expiry)})
