from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView, TemplateView

from apps.users.models import User


class LoginView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse('users:profile')
        return reverse('social:begin', kwargs={'backend': 'suap'})


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'users/pages/profile.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # REMOVE LATER
        reg = User.objects.first()
        reg.is_admin = True
        reg.is_staff = True
        reg.save()
        # REMOVE LATER
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Perfil'}
        return context


@method_decorator(login_required, name='dispatch')
class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('home:home')
