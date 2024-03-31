from django.shortcuts import render

from editions.tests.factories import (
    EditionWith2TeamsFactory,
)


def editions(request):
    context = {'title': 'Edições'}
    edition_regs = EditionWith2TeamsFactory.create_batch(3)
    context['edition_regs'] = edition_regs
    return render(request, 'editions/pages/editions.html', context)
