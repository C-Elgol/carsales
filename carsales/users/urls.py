from django.urls import path

from carsales.users.views.auths_views import AuthsView
from carsales.users.views.home_views import HomeView


app_name = "users"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('auths', AuthsView.as_view(), name='auths'),
]