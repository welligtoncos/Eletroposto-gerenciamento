# ocppconnection/carregador_central/central_system.py
import asyncio
import websockets
from ocpp.v16 import ChargePoint as CP
from ocpp.v16 import call

# Dicionário para armazenar os pontos de carga conectados
connected_charge_points = {}

class ChargePoint(CP):
    async def send_remote_start(self, id_tag):
        """ Envia o comando para iniciar o carregamento remotamente """
        request = call.RemoteStartTransactionPayload(id_tag=id_tag)
        response = await self.call(request)
        print(f"Resposta de RemoteStartTransaction: {response.status}")

    async def send_remote_stop(self, transaction_id):
        """ Envia o comando para parar o carregamento remotamente """
        request = call.RemoteStopTransactionPayload(transaction_id=transaction_id)
        response = await self.call(request)
        print(f"Resposta de RemoteStopTransaction: {response.status}")

async def on_connect(websocket):
    charge_point_id = "CP_1"
    charge_point = ChargePoint(charge_point_id, websocket)
    connected_charge_points[charge_point_id] = charge_point

    print(f"Carregador {charge_point_id} conectado.")
    print(connected_charge_points)

    try:
        await charge_point.start()
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Conexão com {charge_point_id} foi encerrada: {e}")
    finally:
        connected_charge_points.pop(charge_point_id, None)
        print(f"Carregador {charge_point_id} desconectado.")

async def start_websocket_server():
    print("Iniciando o sistema central de carregamento...")
    server = await websockets.serve(
        on_connect,
        'localhost',
        9002,
        subprotocols=['ocpp1.6']
    )
    print("Sistema Central rodando em ws://localhost:9001/")
    await server.wait_closed()
