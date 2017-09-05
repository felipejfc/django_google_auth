# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import GoogleAuthCodeURL, ExchangeCode

urlpatterns = [
    url(r'^code_url/?$', GoogleAuthCodeURL.as_view(), name="codeurl"),
    url(r'^authenticate/?$', ExchangeCode.as_view(), name="authenticate"),
]
