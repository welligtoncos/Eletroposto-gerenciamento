# central_system.py
import asyncio
import websockets
from ocpp.v16 import ChargePoint as CP
from ocpp.v16 import call 

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
    charge_point_id = "CP_1"  # Identificador para o ponto de carga
    charge_point = ChargePoint(charge_point_id, websocket)
    connected_charge_points[charge_point_id] = charge_point

    print(f"Carregador {charge_point_id} conectado.")
    print (connected_charge_points)

    try:
        await charge_point.start()
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Conexão com {charge_point_id} foi encerrada: {e}")
    finally:
        # Remova o ponto de carga desconectado da lista
        connected_charge_points.pop(charge_point_id, None)
        print(f"Carregador {charge_point_id} desconectado.")

async def main():
    server = await websockets.serve(
        on_connect,
        'localhost',
        9001,
        subprotocols=['ocpp1.6']
    )

    print("Sistema Central rodando em ws://localhost:9001/") 

    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
