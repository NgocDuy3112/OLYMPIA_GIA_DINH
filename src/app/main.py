from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.postgresql.database import AsyncPostgresDatabase
from app.api.v0 import (
    answer, 
    team, 
    player, 
    bonus, 
    record_team,
    leaderboard
)
from src.app.api.v0 import record


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db = AsyncPostgresDatabase(dbname="gloryteam")
        await db.connect()

        if not await db.is_connected():
            raise RuntimeError("PostgreSQL connection failed.")

        # Step 3: Initialize SQLAlchemy engine and session
        db_url = db.get_connection_string()
        engine = create_async_engine(db_url, echo=True, future=True)
        async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

        # Store in app state
        app.state.db = db
        app.state.engine = engine
        app.state.postgresql_async_session = async_session_maker

        yield

    except Exception as e:
        print(f"❌ Error during async DB initialization: {e}")
        raise

    finally:
        if hasattr(app.state, "db"):
            await app.state.db.close()
            print("🛑 AsyncPostgres DB connection closed.")
        if hasattr(app.state, "engine"):
            await app.state.engine.dispose()
            print("🛑 SQLAlchemy async engine disposed.")


app = FastAPI(lifespan=lifespan, description="GLORYTEAM API ENDPOINTS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(leaderboard.v0_router)
app.include_router(answer.v0_router)
app.include_router(team.v0_router)
app.include_router(player.v0_router)
app.include_router(record.v0_router)
app.include_router(record_team.v0_router)
app.include_router(bonus.v0_router)



@app.get("/", tags=['Root'])
async def get_status() -> str:
    return "OLYMPIA CUSTOM API IS RUNNING"



@app.get("/health", status_code=200)
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app.api.main:app", host="0.0.0.0", port=8000, reload=True)