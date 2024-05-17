from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from competitions.forms import (
    SportForm,
)
from competitions.models import Sport
from competitions.tests.factories import CategoryFactory
from editions.models import Edition
from helpers.decorators import admin_required


def sports(request):
    cat_masculino = CategoryFactory(name='Masculino')
    cat_feminino = CategoryFactory(name='Feminino')
    cat_misto = CategoryFactory(name='Misto')
    context = {
        'title': 'Competições',
        'page_variant': 'sports',
        'db_regs': Sport.objects.order_by('name'),
        'search_url': reverse('competitions:sports_search'),
    }
    return render(request, 'competitions/pages/sports.html', context)


def sports_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('competitions:sports'))

    db_regs = Sport.objects.filter(name__icontains=querystr).order_by('name')
    context = {
        'title': 'Competições',
        'page_variant': 'sports',
        'db_regs': db_regs,
    }
    return render(request, 'competitions/pages/competitions.html', context)


@login_required
@admin_required
def sports_create(request):
    form = SportForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Criar esporte',
        'form': form,
    }
    if request.POST:
        if form.is_valid():
            cats_m2m = form.cleaned_data['categories']
            form_reg = form.save(commit=True)
            form_reg.categories.add(*cats_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Esporte adicionado com sucesso.')
            return redirect(reverse('competitions:sports'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'competitions/pages/sport-create.html', context)


@login_required
@admin_required
def sports_edit(request, slug):
    obj = get_object_or_404(Sport, slug=slug)
    form = SportForm(request.POST or None, request.FILES or None, instance=obj)
    form.fields['name'].disabled = True
    context = {
        'title': 'Editar esporte',
        'form': form,
    }
    if request.POST:
        if form.is_valid():
            cats_m2m = form.cleaned_data['categories']
            form_reg = form.save(commit=True)
            form_reg.categories.add(*cats_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Esporte editado com sucesso.')
            return redirect(reverse('competitions:sports'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'competitions/pages/sport-create.html', context)


def sports_detailed(request, slug):
    sport = get_object_or_404(Sport, slug=slug)
    editions = Edition.objects.filter(matches__sport_category__sport=sport).distinct()
    editions_matches = dict()
    for edition in editions:
        query_matches = edition.get_matches.filter(sport_category__sport=sport)
        editions_matches.update({edition: query_matches})
    context = {
        'title': f'{sport.name}',
        'sport_name': sport.name,
        'regs': editions_matches,
    }
    return render(request, 'competitions/pages/sport-detailed.html', context)
