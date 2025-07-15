from pydantic import BaseModel, Field
from uuid import uuid4


class BaseDocumentSchema(BaseModel):
    content: str
    metadata: dict = Field(default_factory=dict)

    def __str__(self):
        self.metadata['id'] = str(uuid4())
        return f"content='{self.content}' metadata={self.metadata}"


class Document(BaseDocumentSchema):
    pass