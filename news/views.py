from django.shortcuts import render

from users.models import User


def news(request):
    context = {'title': 'Notícias'}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
    return render(request, 'news/pages/news.html', context)
