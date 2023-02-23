import uuid
import json
from dataclasses import dataclass
from src.data.rooms_data import RoomsData
from src.data.messaging_data import MessagingData

from fastapi import WebSocket


@dataclass
class ConnectionManager:
    '''
        Manages the active connections
    '''

    def __init__(self) -> None:
        '''
            Initializes the active connections
        '''
        self.active_connections: dict[str, WebSocket] = {}
        self.users: dict[str, str] = {}

    async def save_user(self, user_id: str, user_name: str):
        '''
            Saves the user name to the users
        '''
        self.users[user_id] = user_name

    async def connect(self, websocket: WebSocket):
        '''
            Adds the connection to the active connections
        '''
        await websocket.accept()
        user_id = str(uuid.uuid4())
        self.active_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket):
        '''
            Removes the connection from the active connections
        '''
        user_id = self.find_connection_id(websocket)
        del self.active_connections[user_id]
        return user_id

    def find_connection_id(self, websocket: WebSocket):
        '''
            Finds the connection id from the active connections
        '''
        val_list = list(self.active_connections.values())
        key_list = list(self.active_connections.keys())
        user_id = val_list.index(websocket)
        return key_list[user_id]

    async def send_message_to(self, ws: WebSocket, message: str):
        '''
            Sends the message to a specific client
        '''
        await ws.send_text(message)

    async def broadcast(self, message: str):
        '''
            Sends the message to all the clients
        '''
        for connection in self.active_connections.values():
            await connection.send_text(message)
