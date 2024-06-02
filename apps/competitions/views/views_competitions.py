from django.urls import reverse
from django.views.generic.base import RedirectView


class CompetitionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('competitions:sports:home')
