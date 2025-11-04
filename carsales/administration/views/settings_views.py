from django.views.generic import TemplateView

from django.utils.translation import gettext_lazy as _


class SettingView(TemplateView):
    template_name = 'publics/admin/settings/settings.html'
