from django.urls import path

from dominio.login import views


urlpatterns = [
    path('login/', views.login_integra, name="login-integra"),
    path('login-promotron/', views.login_promotron, name="login-promotron"),
]
