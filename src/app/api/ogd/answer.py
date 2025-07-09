from fastapi import APIRouter
from app.schema.v0.answer import AnswerSchema


answers = []
v0_router = APIRouter(prefix="/v1/answers", tags=["Answers - OGD3"])


@v0_router.post("/")
async def create_answer(answer_schema: AnswerSchema):
    answer = answer_schema.model_dump()
    answers.append(answer)
    return answers


@v0_router.get("/")
async def get_answers():
    return answers[-4:]