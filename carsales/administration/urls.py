from django.urls import path

from carsales.administration.views.admin_dashboard_views import AdminDashboardView
from carsales.administration.views.car_management_views import CarManagementView
from carsales.administration.views.customer_views import CustomerView
from carsales.administration.views.review_view import ReviewsView
from carsales.administration.views.settings_views import SettingView



app_name = "administration"

urlpatterns = [
    path('admin-dashboard', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('car-management', CarManagementView.as_view(), name='car_management'),
    path('customer', CustomerView.as_view(), name='customer'),
    path('reviews', ReviewsView.as_view(), name='reviews'),
    path('setting', SettingView.as_view(), name='setting'),
]