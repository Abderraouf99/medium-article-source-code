import json
import uuid
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.models.room import Room
from src.connection_manager.connection_manager import ConnectionManager
from src.logger.logger import Logger
from src.data.rooms_data import RoomsData

from src.data.messaging_data import MessagingData
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection_manager = ConnectionManager()
rooms_manager = RoomsData()
api_logger = Logger("API")


@app.post("/send-user-name/{user_name}")
async def send_user_name(user_name: str):
    '''
        Sends the user name to the client
    '''
    api_logger.info(f"Received user name: {user_name}")

    # 1. Assign a unique id to the user
    user_id = str(uuid.uuid4())

    # 2. Add the user id to the application users
    await connection_manager.save_user(user_id, user_name)

    # 3. Send the user id to the client
    return {"status": "ok", "status_code": 200, "message": "User name received", "id": user_id}


@app.post("/add-room")
async def add_room(room: Room):
    '''
        Sends the room name to the client
    '''
    room = await rooms_manager.add_room(room)
    if room:
        return {"status": "ok", "status_code": 201, "message": "Room created", "room": room.to_dict()}
    return {"status": "error", "status_code": 500, "message": "Internal server error"}


@app.post("/join-room/{room_id}")
async def join_room(room_id: str):
    '''
        Sends the room id to the client
    '''

    return {"status": "ok", "status_code": 200, "message": "Room created"}


@app.get("/get-rooms")
async def get_rooms():
    '''
        Sends the room id to the client
    '''
    return {"status": "ok"}


@app.websocket("/conversation/{conversation_id}")
async def handle_conversation_messaging(websocket: WebSocket,
                                        conversation_id: str):
    '''
        Handles the websocket connection for messaging
    '''
    # Accept the connection from the client
    await connection_manager.connect(websocket)
    try:
        while True:
            # Receive the message from the client
            data = await websocket.receive_text()
            print("Received: ", data)
            # Send the message to all the clients
            await connection_manager.broadcast(data)

    except WebSocketDisconnect:
        # Remove the connection from the list of active connections
        user_id = connection_manager.disconnect(websocket)
        # Broadcast the disconnection of client with id to all the clients
        await connection_manager.broadcast(json.dumps({"type": "disconnected", "id": user_id}))


@app.websocket("/rooms")
async def handle_rooms(websocket: WebSocket):
    '''
        Handles the websocket connection for rooms
    '''
    # Accept the connection from the client
    try:
        await connection_manager.connect(websocket)
        rooms = rooms_manager.get_all_rooms()
        api_logger.info(f"Sending rooms: {len(rooms)}")
        for room in rooms:
            await websocket.send_text(room.name)
        while True:
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        # Remove the connection from the list of active connections
        user_id = connection_manager.disconnect(websocket)
        # Broadcast the disconnection of client with id to all the clients
        await connection_manager.broadcast(json.dumps({"type": "disconnected", "id": user_id}))
