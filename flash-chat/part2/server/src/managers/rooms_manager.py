"""
    Class to manage the rooms listeners
"""
from src.models.room import Room
from src.logger.logger import Logger
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder


class RoomsManager:
    ''' RoomsManager class to manager the rooms listeners '''

    def __init__(self):
        self.rooms_listeners: set[WebSocket] = set([])
        self.logger = Logger("RoomsManager")

    async def add_rooms_listner(self, websocket: WebSocket):
        ''' Adds the websocket connection to the rooms listeners '''
        await websocket.accept()
        self.rooms_listeners.add(websocket)

    async def remove_rooms_listner(self, websocket: WebSocket):
        ''' Removes the websocket connection from the rooms listeners '''
        self.rooms_listeners.remove(websocket)

    async def send_room_to(self, websocket: WebSocket, room: Room):
        ''' Sends the room to a specific client '''
        json_room = jsonable_encoder(room.to_dict())
        await websocket.send_json(json_room)

    async def broadcast_room(self, room: Room):
        ''' Sends the room to all the clients '''
        json_room = jsonable_encoder(room.to_dict())
        self.logger.info(f"Brodcasting to {len(self.rooms_listeners)} clients")
        self.logger.info(f"Broadcasting room: {json_room}")
        bad_clients = []
        for client in self.rooms_listeners:
            try:
                await client.send_json(json_room)
            except Exception:
                bad_clients.append(client)

        for client in bad_clients:
            self.rooms_listeners.remove(client)
