from django.urls import path

from .views import login_integra


urlpatterns = [
    path('login/', login_integra, name="login-integra"),
]
