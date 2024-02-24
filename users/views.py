from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from users.models import User


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:profile'))
    return redirect(reverse('social:begin', kwargs={'backend': 'suap'}))


@login_required(login_url='/login/')
def profile(request):
    context = {'title': 'Perfil'}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
        context['photo_url'] = user.photo.url
    return render(request, 'users/pages/profile.html', context)


@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect(reverse('home:home'))
