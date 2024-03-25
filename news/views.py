from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from helpers.decorators import admin_required
from news.forms import NewsForm
from news.models import News


def news(request):
    news = News.objects.all()
    context = {
        'title': 'Notícias',
        'news_obj': news,
    }
    return render(request, 'news/pages/news.html', context)


@login_required
@admin_required
def create_news(request):
    form = NewsForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Criar notícia',
        'form': form,
        'form_action': reverse('news:create_news'),
    }
    if request.POST:
        if form.is_valid():
            news = form.save(commit=False)
            news.administrator = request.user
            news.save()
            messages.success(request, 'Notícia criada com sucesso.')
            return redirect(reverse('news:news'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'news/pages/create-news.html', context)


# TODO: verify if news has cover
