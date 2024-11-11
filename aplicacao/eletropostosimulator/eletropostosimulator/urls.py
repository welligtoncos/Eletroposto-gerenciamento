from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter() 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ocppconnection.urls')),  # Inclua as URLs do aplicativo ocppconnection
]
