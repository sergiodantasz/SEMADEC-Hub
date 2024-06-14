from django.views.generic.detail import DetailView

from apps.news.models import News
from base.views import MessageMixin
from helpers.model import is_owner


class NewsDetailView(MessageMixin, DetailView):
    model = News
    template_name = 'news/pages/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context |= {
            'title': obj.title,  # type: ignore
            'is_owner': is_owner(self.request.user, obj),  # type: ignore
        }
        return context
