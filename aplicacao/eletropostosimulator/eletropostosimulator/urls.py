from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ocppconnection.views import RemoteStartTransactionView, RemoteStopTransactionView

router = routers.DefaultRouter() 

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('remote-start/', RemoteStartTransactionView.as_view(), name='remote-start'),
    path('remote-stop/', RemoteStopTransactionView.as_view(), name='remote-stop'),
]
