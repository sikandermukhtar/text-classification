from fastapi import APIRouter, Depends
from app.models import User
from app.config.database import get_db
from app.utils.user import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserRead

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/me", response_model=UserRead)
async def get_user(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return current_user