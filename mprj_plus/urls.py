from django.urls import path, include

from rest_framework import routers

from .views import AreaViewSet, TemaViewSet, IconeViewSet


router = routers.DefaultRouter()
router.register('areas', AreaViewSet)
router.register('temas', TemaViewSet)
router.register('icones', IconeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
