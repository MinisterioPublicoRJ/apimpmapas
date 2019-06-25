from django.urls import path

from login.views import LoginView, TestView

app_name = 'login'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('teste', TestView.as_view(), name='teste')
]