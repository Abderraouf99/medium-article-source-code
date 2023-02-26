"""Module providing the RoomsData class to interact with the rooms data"""
import os
from src.models.room import Room
from src.logger.logger import Logger

from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient


class RoomsData:
    '''
    RoomsData class

    '''

    def __init__(self):
        mongo_url = os.getenv("MONGO_URI")
        # use pymongo to connect to the database
        self.client = MongoClient(mongo_url)
        self.data_base = self.client["chat"]
        self.rooms_collection: Collection[Room] = self.data_base["rooms"]
        self.logger = Logger("RoomsData")
        main_room = Room(name="General", description="General room")

        self.add_room(main_room)

    def add_room(self, room: Room) -> Room:
        '''
            Adds a room to the data base
        '''
        # use pymongo to insert the room to the database
        # ensure document is updated if it already exists
        self.logger.info("Adding room to the database")
        try:
            valid_room = Room(**room.to_dict())
            if not valid_room:
                self.logger.error("Invalid room")
                return None
            self.rooms_collection.update_one(
                {"_id": valid_room.name},
                {'$set': valid_room.to_dict()},
                upsert=True
            )
            self.logger.info("Room added to the database")
            return valid_room
        except Exception as error:
            self.logger.error(error)
            return None

    def get_all_rooms(self) -> list[Room]:
        '''
            Gets all rooms from the data base
        '''
        # use pymongo to get the room from the database
        try:
            self.logger.info("Getting all rooms from the database")
            rooms_cursor = self.rooms_collection.find()
            return [Room(**room) for room in rooms_cursor]
        except Exception as error:
            self.logger.error(error)
            return None
