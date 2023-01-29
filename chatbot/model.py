from abc import ABC

from pydantic import BaseModel
from typing import Optional
from vkbottle_types.events import BaseGroupEvent


class ObjectModel(BaseModel):
    id: Optional[str]
    event_id: Optional[str]
    type: Optional[str]
    owner_id: Optional[str]
    text: Optional[str]


class Event(BaseGroupEvent, ABC):
    object: Optional[ObjectModel]

    class Config:
        allow_mutation = True
        validate_assignment = True
        arbitrary_types_allowed = True


class MessageObjectModel(BaseModel):
    conversation_message_id: Optional[int]
    peer_id: Optional[int]
    date: Optional[int]
    from_id: Optional[int]
    event_id: Optional[str]
    text: Optional[str]


class MessageObject(BaseModel):
    message: Optional[MessageObjectModel]


class Message(BaseGroupEvent, ABC):
    object: Optional[MessageObject]

    class Config:
        allow_mutation = True
        validate_assignment = True
        arbitrary_types_allowed = True
