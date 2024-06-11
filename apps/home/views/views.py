from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, ListView, UpdateView

from apps.home.forms import TagForm
from apps.home.models import Tag
from base.views import MessageMixin
from helpers.decorators import admin_required


def home(request):
    context = {'title': 'Início'}
    return render(request, 'home/pages/home.html', context)


def tags(request):
    tags_objs = Tag.objects.order_by('name')
    context = {
        'title': 'Tags',
        'tags': tags_objs,
    }
    return render(request, 'home/pages/tags.html', context)


@login_required
@admin_required
def tags_create(request):
    form = TagForm(request.POST or None)
    context = {
        'title': 'Criar tag',
        'form': form,
    }
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag criada com sucesso.')
            return redirect(reverse('home:tags'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'home/pages/create-tag.html', context)


@login_required
@admin_required
def tags_delete(request, slug):
    tag_obj = get_object_or_404(Tag, slug=slug)
    tag_obj.delete()
    messages.success(request, 'Tag apagada com sucesso.')
    return redirect(reverse('home:tags'))
