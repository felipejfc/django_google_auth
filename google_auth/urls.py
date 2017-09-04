# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import GoogleAuthCodeURL, ExchangeCode

urlpatterns = [
    url(r'^codeUrl/?$', GoogleAuthCodeURL.as_view(), name="codeurl"),
    url(r'^complete/?$', ExchangeCode.as_view(), name="complete"),
]
