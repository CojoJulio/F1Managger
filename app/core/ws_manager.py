from fastapi import WebSocket
import asyncio

from  state.race_state import race_state

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.loop = None

    async def add_connection(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

        if self.loop is None:
            self.loop = asyncio.get_event_loop()

    def handle_ws_command(self, data: dict):
        command = data.get('type')

        if command == 'pause':
            race_state.running = False
            race_state.time_scale = 0.0
            print("Received pause command")

        if command == 'resume':
            race_state.running = True
            race_state.time_scale = 1.0
            print("Received resume command")

        if command == 'set_time_scale':
            new_scale = data.get('value', 1.0)
            race_state.time_scale = new_scale
            print(f"Received time scale change: {new_scale}")

    def remove_connection(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.active_connections.remove(connection)



manager = ConnectionManager()