# -*- coding: utf-8 -*-

import requests
import json
import math

from django.views.generic import View
from django.http import HttpResponse
from oauth2client.client import OAuth2WebServerFlow
from django.conf import settings
from .models import get_users_by_email, create_user, create_google_auth_user, regenerate_app_token
from .authentication import do_authentication, get_token_from_request_header
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

authorized_domains = getattr(settings, 'GOOGLE_AUTH_AUTHORIZED_DOMAINS', ['gmail.com'])
client_id = getattr(settings, 'GOOGLE_AUTH_CLIENT_ID', '')
client_secret = getattr(settings, 'GOOGLE_AUTH_CLIENT_SECRET', '')
scope = getattr(settings, 'GOOGLE_AUTH_SCOPE', 'email profile')
redirect_uri = getattr(settings, 'GOOGLE_AUTH_REDIRECT_URL', 'localhost:8000')
	
flow = OAuth2WebServerFlow(client_id=client_id,
                           client_secret=client_secret,
                           scope=scope,
                           redirect_uri=redirect_uri,
                           prompt='consent',
                           access_type='offline')

def make_flow_with_redirect_uri(redirect_uri):
    return OAuth2WebServerFlow(client_id=client_id,
                               client_secret=client_secret,
                               scope=scope,
                               redirect_uri=redirect_uri,
                               prompt='consent',
                               access_type='offline')

class GoogleAuthCodeURL(View):
    def get(self, request):
        auth_uri = flow.step1_get_authorize_url()
        res = {}
        res['codeUrl'] = auth_uri
        return HttpResponse(json.dumps(res))
    head = get

@method_decorator(csrf_exempt, name='dispatch')
class ExchangeCode(View):
    def post(self, request):
        auth_code = request.GET.get('code')
        redirect_uri = request.GET.get('redirect_uri')
        l_flow = make_flow_with_redirect_uri(redirect_uri) if redirect_uri else flow
        credentials = l_flow.step2_exchange(auth_code)
        email = credentials.id_token.get('email','')
        domain = email.split('@')[1]
        name = credentials.id_token.get('given_name','')
        last_name = credentials.id_token.get('family_name','')
        access_token = credentials.access_token
        refresh_token = credentials.refresh_token
        token_expiry = credentials.token_expiry
        if not domain in authorized_domains:
            return HttpResponse('domain unauthorized: {}'.format(domain), status=401)
        user, _ = create_user(name, last_name, email)
        google_auth_user, _ = create_google_auth_user(user, email, access_token, refresh_token, token_expiry)
        res = {}
        res['token'] = str(google_auth_user.app_token)
        res['email'] = email
        return HttpResponse(json.dumps(res))
    head = post

class RefreshAppToken(View):
    def post(self, request):
        current_token = get_token_from_request_header(request)
        user, app_token = do_authentication(current_token)
        res = {}
        res['token'] = str(regenerate_app_token(app_token))
        return HttpResponse(json.dumps(res))
    head = post
