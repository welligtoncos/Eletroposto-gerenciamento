from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Carregador 
from .serializer import CarregadorSerializer

 
class CarregadorViewSet(viewsets.ModelViewSet):
    queryset = Carregador.objects.all()
    serializer_class = CarregadorSerializer

