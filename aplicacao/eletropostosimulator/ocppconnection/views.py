from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
import asyncio
 

from ocppconnection.serializer import CarregadorSerializer

from .models import Carregador 

from ocppconnection.carregador_central.central_system import connected_charge_points  # Caminho ajustado 

# ViewSet para gerenciar os carregadores (CRUD)
class CarregadorViewSet(viewsets.ModelViewSet):
    queryset = Carregador.objects.all()
    serializer_class = CarregadorSerializer

 

class RemoteStartTransactionView(APIView):
    def post(self, request, *args, **kwargs):
        charge_point_id = request.data.get('charge_point_id', 'CP_1')
        id_tag = request.data.get('id_tag', 'User123')
        print(connected_charge_points)
        if charge_point_id in connected_charge_points:
            print(connected_charge_points)
            charge_point = connected_charge_points[charge_point_id]
            # Envia o comando de forma assíncrona
            asyncio.run(charge_point.send_remote_start(id_tag))
            return Response({"message": "RemoteStartTransaction enviado com sucesso."}, status=status.HTTP_200_OK)
        return Response({"error": "Carregador não conectado."}, status=status.HTTP_404_NOT_FOUND)


class RemoteStopTransactionView(APIView):
    def post(self, request, *args, **kwargs):
        charge_point_id =  'CP_1'
        transaction_id = request.data.get('transaction_id', 1) 
        print(connected_charge_points)
        charge_point = connected_charge_points[charge_point_id]
        # Envia o comando de forma assíncrona
        asyncio.run(charge_point.send_remote_stop(transaction_id))
        return Response({"message": "RemoteStopTransaction enviado com sucesso."}, status=status.HTTP_200_OK)
        return Response({"error": "Carregador não conectado."}, status=status.HTTP_404_NOT_FOUND)
