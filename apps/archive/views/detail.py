from typing import Any

from django.views.generic.detail import DetailView

from apps.home.models import Collection
from helpers.model import is_owner


class ArchiveDetailView(DetailView):
    model = Collection
    template_name = 'archive/pages/archive_detail.html'
    context_object_name = 'archive'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context |= {
            'title': obj.title,  # type: ignore
            'is_owner': is_owner(self.request.user, obj),  # type: ignore
        }
        return context
