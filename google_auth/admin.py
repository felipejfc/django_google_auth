# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import GoogleAuthUser

class GoogleAuthUserOption(admin.ModelAdmin):
    """GoogleAuthUser options"""
    list_display = ('email','app_token','access_token','refresh_token','token_expiry')
    search_fields = ('email',)

admin.site.register(GoogleAuthUser, GoogleAuthUserOption)
