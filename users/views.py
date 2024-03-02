import os
from pathlib import Path

from authlib.integrations.django_client import OAuth
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User as DjangoUser
from django.contrib.sessions.models import Session
from django.shortcuts import redirect, render
from django.urls import reverse

from suap.backends import SuapOAuth2, UserData, create_user_model_registry
from users.models import User

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
oauth = SuapOAuth2()


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:profile'))

    redirect_uri = request.build_absolute_uri('/complete/suap/')
    return oauth.authorize_redirect(request, redirect_uri)


def suap(request):
    token = oauth.authorize_access_token(request)
    response = oauth.get('eu', token=token)
    response['curso'] = (
        oauth.get('v2/minhas-informacoes/meus-dados/?format=json', token=token)
        .get('vinculo')
        .get('curso')
    )
    user_emails = (
        response.get('email_secundario'),
        response.get('email_google_classroom'),
        response.get('email_academico'),
    )
    obj = UserData(response)
    user_reg = create_user_model_registry(obj, user_emails)
    request.session['userreg'] = user_reg.registration
    return redirect(reverse('users:profile'))


def profile(request):
    context = {'title': 'Perfil'}
    registration = request.session.get('userreg')
    if registration:
        user = User.objects.get(registration=registration)
        context['user'] = user  # type: ignore
    return render(request, 'users/pages/profile.html', context)


def logout(request):
    auth_logout(request)
    return redirect(reverse('home:home'))
