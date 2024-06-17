from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from apps.editions.models import Edition
from apps.home.forms import TagForm
from apps.home.models import Collection, Tag
from apps.news.models import News
from helpers.decorators import admin_required


class HomeView(TemplateView):
    template_name = 'home/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_edition = Edition.objects.order_by('-year').first()
        context |= {
            'title': 'Início',
            'last_edition': last_edition or '',
            'news': News.objects.all(),
            'document_collection': Collection.objects.filter(collection_type='document')
            .order_by('-created_at')
            .first()
            or '',
            'archive': Collection.objects.filter(collection_type='image')
            .order_by('-created_at')
            .first(),
            'matches': '' if not last_edition else last_edition.matches.all(),
        }
        return context


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
