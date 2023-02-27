"""Main app server"""
import uuid
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status, Response
from fastapi.middleware.cors import CORSMiddleware

from src.models.room import Room
from src.models.chat_message import ChatMessage
from src.managers.rooms_manager import RoomsManager
from src.managers.messaging_manager import MessagingManager
from src.logger.logger import Logger
from src.data.rooms_data import RoomsData
from src.data.messaging_data import MessageData

# Instance of the FastAPI app
app = FastAPI()

# Adding the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creating the managers
chat_manager = MessagingManager()
rooms_manager = RoomsManager()

# Creating the data
rooms_data = RoomsData()
messages_data = MessageData()

# Creating the logger
api_logger = Logger("API")

@app.post("/add-room/", status_code=status.HTTP_201_CREATED)
async def handle_add_room(room: Room, response: Response):
    '''
        Function to handle new room created by a client
    '''
    room = rooms_data.add_room(room)
    if room:
        await rooms_manager.broadcast_room(room)
        return {"message": "Room added"}
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": "Room not added"}


@app.websocket("/connect-rooms/{room_id}")
async def handle_connect_to_room(websocket: WebSocket,
                                        room_id: str):
    '''
        Function to handle connections to a room
        The function accepts the connection from the client
        and sends the messages to the client
    '''
    # Accept the connection from the client
    await chat_manager.connect(websocket, room_id)

    # Sending the messages to the new client
    messages = messages_data.get_messages_of(room_id)
    for message in messages:
        api_logger.info("Sending message to new client")
        await chat_manager.send_message_to(websocket, message)

    try:
        while True:
            # Receive the message from the client
            data = await websocket.receive_json()
            api_logger.info(f"Received {data}")

            if "type" in data and data["type"] == "close":
                chat_manager.disconnect(websocket, room_id)
            else:
                message = ChatMessage(
                    message_id=str(uuid.uuid4()),
                    user_id=data["user_id"],
                    message=data["message"],
                    room_id=data["room_id"]
                )
                messages_data.add_message(message)
                # Send the message to all the clients
                await chat_manager.broadcast(message, room_id)

    except WebSocketDisconnect:
        # Remove the connection from the list of active connections
        api_logger.info("Client disconnected")
        chat_manager.disconnect(websocket, room_id)


@app.websocket("/rooms")
async def handle_new_connection_rooms(websocket: WebSocket):
    '''
        Function to handle new conenctions to the rooms
        The function accepts the connection from the client
        and sends all the available rooms to the client
    '''
    try:
        await rooms_manager.add_rooms_listner(websocket)
        rooms = rooms_data.get_all_rooms()
        api_logger.info(f"Sending rooms: {len(rooms)}")
        for room in rooms:
            await rooms_manager.send_room_to(websocket, room)
        while True:
            # we keep the connection alive
            # when a new room is created by a client
            # we broadcast the new room to all the clients
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        await rooms_manager.remove_rooms_listner(websocket)
