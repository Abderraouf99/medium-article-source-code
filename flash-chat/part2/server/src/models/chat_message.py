"""
    Model class for chat messages
"""
from pydantic import BaseModel


class ChatMessage(BaseModel):
    '''
        Chat message dataclass
    '''
    message_id: str
    user_id: str
    message: str
    room_id: str

    def to_dict(self) -> dict:
        '''
            Converts the dataclass to a dictionary
        '''
        return {
            'message_id': self.message_id,
            'message': self.message,
            'user_id': self.user_id,
            'room_id': self.room_id
        }
