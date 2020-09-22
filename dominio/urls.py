from django.urls import include, path


app_name = 'dominio'

urlpatterns = [
    path('token/', include("dominio.login.urls")),
    path("alertas/", include("dominio.alertas.urls")),
    path("pip/", include("dominio.pip.urls")),
    path("suamesa/", include("dominio.suamesa.urls")),
    path("", include("dominio.tutela.urls")),
]
