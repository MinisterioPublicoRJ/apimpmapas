from django.urls import path, include

from rest_framework import routers

from .views import AreaViewSet, TemaViewSet


router = routers.DefaultRouter()
router.register('areas', AreaViewSet)
router.register('temas', TemaViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
