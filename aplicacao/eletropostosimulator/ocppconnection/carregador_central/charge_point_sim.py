# charge_point_sim.py
import asyncio
import websockets
from ocpp.v16 import ChargePoint as CP

class ChargePoint(CP):
    async def start(self):
        print("Simulador de Ponto de Carga Iniciado.")
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Simulador de Ponto de Carga encerrado.")
        finally:
            print("Conexão finalizada.")

async def main():
    uri = "ws://localhost:9002/CP_1"  # Certifique-se de que o URI está correto
    try:
        async with websockets.connect(uri, subprotocols=['ocpp1.6']) as websocket:
            charge_point_id = "CP_1"
            charge_point = ChargePoint(charge_point_id, websocket)
            await charge_point.start()
    except Exception as e:
        print(f"Erro ao conectar ao sistema central: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário.")
