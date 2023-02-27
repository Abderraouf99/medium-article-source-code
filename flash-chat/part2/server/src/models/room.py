""" Model class for chat rooms """
import json
from pydantic import BaseModel


class Room (BaseModel):
    '''
        Room dataclass for the chat
    '''

    name: str
    description: str

    def to_dict(self):
        '''
            Converts the room to a dictionary
        '''
        return {
            '__id:': self.name,
            'name': self.name,
            'description': self.description,
        }