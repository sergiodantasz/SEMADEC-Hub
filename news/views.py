from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.models import User


@login_required(login_url='/login/')
def news(request):
    context = {'title': 'Notícias'}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
    return render(request, 'news/pages/news.html', context)
