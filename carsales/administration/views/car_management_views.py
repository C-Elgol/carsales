from django.views.generic import TemplateView

from django.utils.translation import gettext_lazy as _


class CarManagementView(TemplateView):
    template_name = 'publics/admin/car_management/car_management.html'
