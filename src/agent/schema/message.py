from pydantic import BaseModel, Field


class BaseMessageSchema(BaseModel):
    role: str = Field(..., description="Role of the message sender (e.g., 'user', 'assistant', 'system')")
    content: str = Field(..., description="Content of the message")


class Message(BaseMessageSchema):
    pass