from django.urls import include, path


app_name = "proxies"
urlpatterns = [
    path("", include("proxies.detran.urls")),
]
