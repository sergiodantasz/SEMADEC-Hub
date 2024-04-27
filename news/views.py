from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from helpers.decorators import admin_required
from helpers.model import is_owner
from news.forms import NewsForm
from news.models import News


def news(request):
    news_objs = News.objects.order_by('-created_at')
    context = {
        'title': 'Notícias',
        'db_regs': news_objs,
        'search_url': reverse('news:search_news'),
    }
    return render(request, 'news/pages/news.html', context)


def search_news(request):
    query = request.GET.get('q').strip()
    if not query:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('news:news'))
    news_objs = News.objects.filter(
        Q(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(content__icontains=query)
        )
    ).order_by('-created_at')
    context = {
        'db_regs': news_objs,
        'search_url': reverse('news:search_news'),
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
            form.save_m2m()
            messages.success(request, 'Notícia criada com sucesso.')
            return redirect(reverse('news:news'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'news/pages/create-news.html', context)


@login_required
@admin_required
def delete_news(request, slug):
    news_obj = get_object_or_404(News, slug=slug)
    if not is_owner(request.user, news_obj):
        raise PermissionDenied()
    news_obj.delete()
    messages.success(request, 'Notícia apagada com sucesso.')
    return redirect(reverse('news:news'))


@login_required
@admin_required
def edit_news(request, slug):
    news_obj = get_object_or_404(News, slug=slug)
    if not is_owner(request.user, news_obj):
        raise PermissionDenied()
    form = NewsForm(request.POST or None, request.FILES or None, instance=news_obj)
    context = {
        'title': 'Editar notícia',
        'news': news_obj,
        'form': form,
        'form_action': reverse('news:edit_news', kwargs={'slug': news_obj.slug}),
    }
    if request.POST:
        if form.is_valid():
            news = form.save()
            messages.success(request, 'Notícia editada com sucesso.')
            return redirect(reverse('news:news'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'news/pages/edit-news.html', context)


def view_news(request, slug):
    news_obj = get_object_or_404(News, slug=slug)
    context = {
        'title': news_obj.title,
        'news': news_obj,
        'is_owner': is_owner(request.user, news_obj),
    }
    return render(request, 'news/pages/view-news.html', context)
