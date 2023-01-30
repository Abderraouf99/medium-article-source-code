from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dataclasses import dataclass
from typing import List


@dataclass
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message_to(self, target: WebSocket, message: str):
        await target.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


app = FastAPI()

connection_manager = ConnectionManager()


@app.websocket("/messaging")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print("Received: ", data)
            await connection_manager.broadcast(data)

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"Client left the chat")
