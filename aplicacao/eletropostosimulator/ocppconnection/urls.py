from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CarregadorViewSet

router = DefaultRouter()
router.register(r'carregadores', CarregadorViewSet, basename='carregador')

urlpatterns = [
    path('', include(router.urls)),
]
