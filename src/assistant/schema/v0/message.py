from pydantic import BaseModel, Field


class BaseMessageSchema(BaseModel):
    role: str = Field(..., description="Role of the message sender (e.g., 'user', 'assistant', 'system')")
    content: str = Field(..., description="Content of the message")

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content
        }


class Message(BaseMessageSchema):
    pass