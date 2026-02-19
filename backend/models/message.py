from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid
from .user import User
from .conversation import Conversation


class MessageBase(SQLModel):
    conversation_id: uuid.UUID
    role: str  # 'user' or 'assistant'
    content: str


class Message(MessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    role: str  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="messages")
    conversation: Conversation = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessagePublic(MessageBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime