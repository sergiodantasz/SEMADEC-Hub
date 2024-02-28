import os

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from requests_oauthlib import OAuth2Session

from suap.backends import SuapOAuth2
from users.models import User

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def suap(request):
    suap_uri = request.build_absolute_uri()
    SuapOAuth2.fetch_token(suap_uri)
    r = SuapOAuth2.get('https://suap.ifrn.edu.br/api/eu/')
    y = SuapOAuth2.get('https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/')
    return HttpResponse(f'<p>{r.text}, {y.text}</p>')


def login(request):
    return redirect(SuapOAuth2.authorization_url)


@login_required(login_url='/login/')
def profile(request):
    context = {'title': 'Perfil'}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
    return render(request, 'users/pages/profile.html', context)


@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect(reverse('home:home'))
