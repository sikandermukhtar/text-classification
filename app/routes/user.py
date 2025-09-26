from fastapi import APIRouter, Depends
from app.models import User
from app.config.database import get_db
from app.utils.user import get_current_user
from sqlalchemy.orm import Session
from app.schemas import UserRead

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/me", response_model=UserRead)
def get_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user