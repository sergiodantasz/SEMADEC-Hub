from django.shortcuts import render

from users.models import User


def home(request):
    context = {'title': 'Início'}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
    return render(request, 'home/pages/home.html', context)
