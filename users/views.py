from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from users.models import User


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:profile'))
    return redirect(reverse('social:begin', kwargs={'backend': 'suap'}))


@login_required
def profile(request):
    context = {'title': 'Perfil'}
    # REMOVE LATER
    # reg = User.objects.first()
    # reg.is_admin = True
    # reg.is_staff = True
    # reg.save()
    # REMOVE LATER
    return render(request, 'users/pages/profile.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse('home:home'))
