from fastapi import APIRouter, WebSocket, Depends
from valkey.asyncio import Valkey

from app.dependencies.db import get_valkey_pubsub
from app.core.ws import handle_match_websocket


ws_router = APIRouter(prefix="/ws", tags=["WebSocket"])



@ws_router.websocket("/match/{match_code}")
async def match_websocket_endpoint(
    websocket: WebSocket,
    match_code: str,
    valkey: Valkey = Depends(get_valkey_pubsub),
):
    """
    WebSocket endpoint for a match.
    Clients subscribe to real-time updates for a match.
    """
    await handle_match_websocket(websocket, match_code, valkey)