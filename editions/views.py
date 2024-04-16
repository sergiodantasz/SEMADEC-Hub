from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from editions.models import Edition, Team
from editions.tests.factories import (
    EditionWith2TeamsFactory,
    TeamFactory,
)
from helpers.decorators import admin_required

from .forms import EditionForm


def editions(request):
    EditionWith2TeamsFactory.create_batch(3)  # Remove if needed
    # TeamFactory.create_batch(5)
    context = {
        'title': 'Edições',
        'db_regs': Edition.objects.all(),
    }
    return render(request, 'editions/pages/editions.html', context)


@login_required
@admin_required
def editions_create(request):
    form = EditionForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Adicionar edição',
        'form': form,
        'form_action': reverse('editions:editions_create'),
    }
    if request.POST:
        if form.is_valid():
            teams_m2m = form.cleaned_data['teams']
            form_reg = form.save(commit=True)
            form_reg.teams.add(*teams_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Edição adicionada com sucesso.')
            return redirect(reverse('editions:editions'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'editions/pages/edition-create.html', context)
