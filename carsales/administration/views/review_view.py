from django.views.generic import TemplateView

from django.utils.translation import gettext_lazy as _


class ReviewsView(TemplateView):
    template_name = 'publics/admin/reviews/reviews.html'
