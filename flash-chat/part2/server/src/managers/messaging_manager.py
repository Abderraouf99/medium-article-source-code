"""
    Class to manage the messaging
"""
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from src.logger.logger import Logger
from src.models.chat_message import ChatMessage


class MessagingManager:
    '''
        Manages the active connections
    '''

    def __init__(self) -> None:
        '''
            Initializes the active connections
        '''
        self.active_connections: dict[str, set[WebSocket]] = {}
        self.users_id_name: dict[str, str] = {}
        self.logger = Logger("MessagingManager")

    async def save_user(self, user_id: str, user_name: str):
        '''
            Saves the user name to the users
        '''
        self.users_id_name[user_id] = user_name

    async def connect(self, websocket: WebSocket, room_id: str):
        '''
            Adds the connection to the active connections
        '''
        # Accept the user connection
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()

        self.active_connections[room_id].add(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        '''
            Removes the connection from the active connections
        '''
        self.active_connections[room_id].remove(websocket)

    async def send_message_to(self, websocket: WebSocket, message: ChatMessage):
        '''
            Sends the message to a specific client
        '''
        json_message = jsonable_encoder(message.to_dict())
        await websocket.send_json(json_message)

    async def broadcast(self, message: ChatMessage, room_id: str):
        '''
            Sends the message to all the clients
        '''
        self.logger.info(
            f"Broadcasting message to {len(self.active_connections[room_id])} clients")
        for connection in self.active_connections[room_id]:
            await self.send_message_to(connection, message)
