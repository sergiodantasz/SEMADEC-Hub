from django.shortcuts import redirect
from django.urls import reverse


def competitions(request):
    return redirect(reverse('competitions:sports:home'))
