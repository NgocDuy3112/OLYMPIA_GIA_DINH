from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Annotated


class BaseAnswerSchema(BaseModel):
    index: int = Field(gt=0, lt=4)
    name: str = Field(min_length=1)
    answer: str = Field()
    time: Annotated[Decimal, Field(decimal_places=3)]


class AnswerSchema(BaseAnswerSchema):
    pass