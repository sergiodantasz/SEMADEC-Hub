import os
from dataclasses import asdict

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.shortcuts import redirect, render
from django.urls import reverse
from requests_oauthlib import OAuth2Session

from suap.backends import (
    SuapOAuth2,
    UserData,
    create_emails,
    create_user_model_registry,
)
from users.models import User

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def suap(request):
    suap_uri = request.build_absolute_uri()
    SuapOAuth2.fetch_token(suap_uri)
    response = SuapOAuth2.get('https://suap.ifrn.edu.br/api/eu/?format=json').json()
    response['curso'] = (
        SuapOAuth2.get(
            'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/?format=json'
        )
        .json()
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
    user_reg.save()
    user_auth = DjangoUser.objects.create(
        first_name=obj.first_name,
        last_name=obj.last_name,
        username=obj.registration,
        email='joamersonislan38@gmail.com',
    )
    user_auth.set_unusable_password()
    user_auth.save()
    authenticated_user = authenticate(request, username=obj.registration).first()
    request.user = authenticated_user
    ...
    return profile(request)


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:profile'))
    return redirect(SuapOAuth2.authorization_url)


def profile(request):
    context = {'title': 'Perfil'}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
    return render(request, 'users/pages/profile.html', context)


# @login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect(reverse('home:home'))
