from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.dependencies import engine
from app.api import (
    player,
    team,
    match,
    answer,
    record
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Database engine initialized")
    yield
    print("Application Shutdown: Disposing of database engine.")
    if engine: await engine.dispose()



app = FastAPI(lifespan=lifespan, description="OLYMPIA GIA ĐỊNH 3")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(player.player_router)
app.include_router(team.team_router)
app.include_router(match.match_router)
app.include_router(answer.answer_router)
app.include_router(record.record_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app.api.main:app", host="0.0.0.0", port=8000, reload=True)