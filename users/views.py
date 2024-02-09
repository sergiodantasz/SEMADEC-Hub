from django.shortcuts import redirect, render
from django.urls import reverse


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:profile'))
    return redirect(reverse('social:begin', kwargs={'backend': 'suap'}))
