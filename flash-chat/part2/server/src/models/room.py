import json
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass()
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
            '__id': self.name,
            'name': self.name,
            'description': self.description,
        }

    def to_json(self):
        '''
            Converts the room to a json
        '''
        return json.dumps(self.__dict__)
