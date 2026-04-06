from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from app.config.database import get_db
from .jwt import decode_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(request: Request, token: str = Depends(oauth_scheme), db: AsyncSession = Depends(get_db)):
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        token = cookie_token

    payload = decode_token(token)
    email = payload["sub"]
    
    # Use asynchronous select query
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="No user found!")
    return user
