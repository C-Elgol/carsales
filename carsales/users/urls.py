from django.urls import path

from carsales.users.views.home_views import HomeView


app_name = "users"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]