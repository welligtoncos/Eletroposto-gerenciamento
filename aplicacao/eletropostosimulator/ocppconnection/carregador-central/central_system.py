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

async def on_connect(websocket, path):
    charge_point_id = path.strip('/')
    charge_point = ChargePoint(charge_point_id, websocket)
    connected_charge_points[charge_point_id] = charge_point

    print(f"Carregador {charge_point_id} conectado.")

    await charge_point.start()

async def main():
    server = await websockets.serve(
        on_connect,
        'localhost',
        9001,
        subprotocols=['ocpp1.6']
    )

    print("Sistema Central rodando em ws://localhost:9000/")

    # Aguardar conexão do carregador
    await asyncio.sleep(2)

    # Enviar comandos para ligar e desligar a carga
    cp_id = 'CP_1'
    id_tag = 'User123'
    transaction_id = 1  # Um ID fictício de transação

    if cp_id in connected_charge_points:
        charge_point = connected_charge_points[cp_id]
        # Enviar comando para ligar o carregador
        await charge_point.send_remote_start(id_tag)
        # Aguardar 5 segundos simulando carregamento
        await asyncio.sleep(5)
        # Enviar comando para desligar o carregador
        await charge_point.send_remote_stop(transaction_id)
    else:
        print(f"Carregador {cp_id} não está conectado.")

    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
