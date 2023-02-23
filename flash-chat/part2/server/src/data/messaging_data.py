"""Module providing the MessagingData class to interact with the messaging data"""
import os
from src.models.chat_message import ChatMessage
from src.logger.logger import Logger

from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection


class MessagingData:
    '''
        This class is responsible for storing messaging to the client.
    '''

    def __init__(self) -> None:
        '''
            Initializes the messaging
        '''
        mongo_url = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_url)
        self.data_base = self.client["chat"]
        self.messages_collection: Collection[ChatMessage] = self.data_base["messages"]
        self.logger = Logger("MessagingData")

    def add_message(self, message: ChatMessage):
        '''
            Adds a message to the list
        '''
        try:
            # use pymongo to insert the message to the database
            # ensure document is updated if it already exists
            self.logger.info("Adding message to the database")

            self.messages_collection.update_one(
                {
                    '__id': message.message_id,
                    'room_id': message.id
                },
                {'$setOnInsert': message},
                upsert=True
            )
        except TypeError as error:
            self.logger.error(f"Error adding message to the database: {error}")
        except ValueError as error:
            self.logger.error(f"Error adding message to the database: {error}")
        except Exception as error:
            self.logger.error(f"Error adding message to the database: {error}")

    def get_messages_of(self, room_id: str) -> list[ChatMessage]:
        '''
            Gets the messages of a specific room
        '''
        try:
            return self.messages_collection.find({'room_id': room_id})
        except TypeError as error:
            self.logger.error(
                f"Error getting messages from the database: {error}")
            return []
        except ValueError as error:
            self.logger.error(
                f"Error getting messages from the database: {error}")
            return []
        except Exception as error:
            self.logger.error(
                f"Error getting messages from the database: {error}")
            return []
