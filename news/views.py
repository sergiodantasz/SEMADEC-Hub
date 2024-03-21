from django.shortcuts import render


def news(request):
    context = {'title': 'Notícias'}
    return render(request, 'news/pages/news.html', context)
