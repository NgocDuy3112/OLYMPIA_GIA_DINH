from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schema.user import *
from app.model.user import User
from app.core.security import *
from app.dependencies.db import get_db


auth_router = APIRouter(prefix="/auth", tags=["Uỷ Quyền"])



@auth_router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    # Check if username exists
    result = await session.execute(select(User).where(User.username == user_data.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    token = create_access_token({"sub": new_user.username, "role": new_user.role})
    return TokenResponse(access_token=token)



@auth_router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "role": user.role})
    return TokenResponse(access_token=token, token_type="bearer")