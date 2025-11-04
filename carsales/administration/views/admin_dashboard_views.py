from django.views.generic import TemplateView

from django.utils.translation import gettext_lazy as _


class AdminDashboardView(TemplateView):
    template_name = 'publics/admin/admin_dashboard.html'
