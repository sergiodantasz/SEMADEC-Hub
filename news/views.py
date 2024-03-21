from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from news.models import News
from news.tests.factories import NewsFactory


def news(request):
    reg_test = NewsFactory.create_batch(5)  # Remove later
    context = {'title': 'Notícias'}
    return render(request, 'news/pages/news.html', context)


def news_detailed(request, slug):
    news = get_object_or_404(News, slug=slug)
    context = {'title': news.title}
    context['news'] = news
    return render(request, 'news/pages/news_detailed.html', context)