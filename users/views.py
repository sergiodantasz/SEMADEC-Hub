import os

from authlib.integrations.django_client import OAuth
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.urls import reverse

from suap.backends import SuapOAuth2, UserData, get_or_create_user_model_registry
from users.models import User

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
oauth = SuapOAuth2()


def login(request):
    registration = request.session.get('userreg')
    if registration:
        return redirect(reverse('users:profile'))
    redirect_uri = request.build_absolute_uri('/complete/suap/')
    return oauth.authorize_redirect(request, redirect_uri)


def suap(request):
    token = oauth.authorize_access_token(request)
    response = oauth.get_user_data(token)
    user_emails = (
        response.get('email_secundario'),
        response.get('email_google_classroom'),
        response.get('email_academico'),
    )
    obj = UserData(response)
    user_reg = get_or_create_user_model_registry(obj, user_emails)
    request.session['userreg'] = user_reg.registration
    return redirect(reverse('users:profile'))


def profile(request):
    context = {'title': 'Perfil'}
    registration = request.session.get('userreg')
    if registration:
        user = User.objects.get(registration=registration)
        context['user'] = user  # type: ignore
        return render(request, 'users/pages/profile.html', context)
    return redirect(reverse('users:login'))


def logout(request):
    auth_logout(request)
    return redirect(reverse('home:home'))
