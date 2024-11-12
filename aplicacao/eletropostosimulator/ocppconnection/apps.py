# ocppconnection/apps.py
from django.apps import AppConfig
import threading
import asyncio
from ocppconnection.carregador_central.central_system import start_websocket_server  # Importe o servidor WebSocket

class OcppconnectionConfig(AppConfig):
    name = 'ocppconnection'

    def ready(self):
        # Inicie o servidor WebSocket em uma nova thread para rodar em paralelo com o Django
        thread = threading.Thread(target=lambda: asyncio.run(start_websocket_server()), daemon=True)
        thread.start()
