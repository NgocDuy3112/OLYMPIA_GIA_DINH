from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Mapping roles to allowed HTTP verbs
ROLE_PERMISSIONS = {
    "guest": {"GET"},
    "player": {"GET"},
    "moderator": {"GET", "POST", "PUT"},
    "admin": {"GET", "POST", "PUT", "DELETE"},
}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"username": username, "role": role}
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def authorize_user(request: Request, user: dict = Depends(get_current_user)):
    method = request.method.upper()
    user_role = user["role"]
    allowed_methods = ROLE_PERMISSIONS.get(user_role, set())

    if method not in allowed_methods:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{user_role}' is not allowed to perform {method}"
        )
    return user


def get_ws_user(token: str) -> dict:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # Ensure player_code exists for WS usage
    player_code = payload.get("player_code")
    if not player_code:
        raise HTTPException(status_code=401, detail="Token missing player_code")

    # Optionally include role if you want WS authorization later
    return {
        "username": payload.get("sub"),
        "player_code": player_code,
        "role": payload.get("role", "guest"),  # default guest
    }