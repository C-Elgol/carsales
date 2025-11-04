from django.views.generic import TemplateView

from django.utils.translation import gettext_lazy as _


class AuthsView(TemplateView):
    template_name = 'publics/auth/forms.html'
