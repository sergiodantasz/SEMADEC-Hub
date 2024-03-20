from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from news.models import News
from news.tests.factories import NewsFactory
from users.models import User


@login_required(login_url='/login/')
def news(request):
    reg_test = NewsFactory.create_batch(5)  # Remove later
    context = {'title': 'Notícias'}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
        context['news_list'] = reg_test
    return render(request, 'news/pages/news.html', context)


@login_required(login_url='/login/')
def news_detailed(request, slug):
    try:
        news = get_object_or_404(News, slug=slug)
        context = {'title': news.title}
        context['news'] = news
        return render(request, 'news/pages/news_detailed.html', context)

    except Http404:
        ...  # Render fallback 404 page
