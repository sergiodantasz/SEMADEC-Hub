from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.home.views.views import MessageMixin
from apps.news.forms import NewsForm
from apps.news.models import News
from helpers.decorators import admin_required
from helpers.model import is_owner


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class NewsCreateView(MessageMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/pages/news_form.html'
    success_url = reverse_lazy('news:list')
    success_message = 'Notícia criada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | {'title': 'Criar notícia'}
        return context

    def form_valid(self, form):
        news = form.save(commit=False)
        news.administrator = self.request.user
        news.save()
        form.save_m2m()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class NewsEditView(MessageMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/pages/news_form.html'
    success_url = reverse_lazy('news:list')
    success_message = 'Notícia editada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) | {'title': 'Editar notícia'}
        return context

    def get(self, request, *args, **kwargs):
        if not is_owner(request.user, self.get_object()):  # type: ignore
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class NewsDeleteView(MessageMixin, DeleteView):
    model = News
    success_url = reverse_lazy('news:list')
    success_message = 'Notícia apagada com sucesso.'

    def get(self, request, *args, **kwargs):
        if not is_owner(request.user, self.get_object()):  # type: ignore
            raise PermissionDenied()
        self.delete(request, *args, **kwargs)
        return redirect(self.success_url)