from django.urls import path

from .views import (
    SuaMesaView
)


urlpatterns = [
    path(
        "suamesa/<str:orgao_id>",
        SuaMesaView.as_view(),
        name="suamesa-teste",
    )
]