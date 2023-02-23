from dataclasses import dataclass
from pydantic import BaseModel


@dataclass(frozen=True)
class ChatMessage(BaseModel):
    '''
        Chat message dataclass
    '''
    message_id: str
    message: str
    user: str
    timestamp: str
    room_id: str
