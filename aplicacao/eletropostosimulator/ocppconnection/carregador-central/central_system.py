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
    charge_point_id = "CP_1"
    charge_point = ChargePoint(charge_point_id, websocket)
    connected_charge_points[charge_point_id] = charge_point

    print(f"Carregador {charge_point_id} conectado.")

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

    print("Sistema Central rodando em ws://localhost:9000/")

    # Loop principal para monitorar pontos conectados
    while True:
        await asyncio.sleep(1)
        if "CP_1" in connected_charge_points:
            # Verifica se o ponto de carga está conectado
            charge_point = connected_charge_points["CP_1"]
            id_tag = 'User123'
            transaction_id = 1
            try:
                # Inicia a transação remotamente
                await charge_point.send_remote_start(id_tag)
                await asyncio.sleep(5)  # Simula o carregamento
                # Para a transação remotamente
                await charge_point.send_remote_stop(transaction_id)
            except Exception as e:
                print(f"Erro ao comunicar com o ponto de carga: {e}")
        else:
            print("Aguardando conexão do Carregador CP_1...")

    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
