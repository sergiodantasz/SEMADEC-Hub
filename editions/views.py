from django.shortcuts import render

from editions.models import Edition
from editions.tests.factories import (
    EditionWith2TeamsFactory,
)


def editions(request):
    EditionWith2TeamsFactory.create_batch(3)  # Remove if needed
    context = {
        'title': 'Edições',
        'db_regs': Edition.objects.all(),
    }
    return render(request, 'editions/pages/editions.html', context)
