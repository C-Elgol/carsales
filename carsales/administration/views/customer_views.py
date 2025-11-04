from django.views.generic import TemplateView

from django.utils.translation import gettext_lazy as _


class CustomerView(TemplateView):
    template_name = 'publics/admin/customers_management/customers.html'
