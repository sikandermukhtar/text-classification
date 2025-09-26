from fastapi import Response
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User, VerificationToken
from app.config.database import get_db
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.utils.jwt import create_access_token
from app.schemas import UserCreate, UserRead, UserLogin, UserLoginSuccess
from app.utils.hashing import hash, verify_hash
from sqlalchemy.exc import IntegrityError
from app.utils.verification_token_gen import generate_secret_token
from datetime import datetime, timezone, timedelta
from email_validator import validate_email, EmailNotValidError

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/signup", response_model=UserRead)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    
    filters = [
        (User.username == user.username),
        (User.email == user.email)
    ]

    if user.phone_number is not None:
        filters.append(User.phone_number == user.phone_number)

    existing_user = db.query(User).filter(or_(*filters)).first()

    if existing_user:
        if existing_user.username == user.username:
            detail = "Username is already taken."
        elif existing_user.email == user.email:
            detail = "Email is already registered."
        elif(user.phone_number is not None and existing_user.phone_number == user.phone_number):
            detail = "Phone number is already registered."
        else:
            detail = "Duplicate entry found"
        raise HTTPException(status_code=400, detail=detail)
    
    
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.")
    
    hashed_password = hash(user.password)

    new_user = User(
        username = user.username,
        email = user.email,
        phone_number = user.phone_number,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.flush()

    verification_token = generate_secret_token()

    user_verification_token = VerificationToken(
        token = verification_token,
        user_id = new_user.id,
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    )

    db.add(user_verification_token)

    try: 
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Request failed, try again."
        )
    
    return new_user


@router.post("/login", response_model=UserLoginSuccess)
def login(user: UserLogin, response: Response, db:Session = Depends(get_db)):

    try:
        email = validate_email(user.identifier,check_deliverability=False)
        existing_user = db.query(User).filter(User.email == user.identifier).first()
    except EmailNotValidError:
        existing_user = db.query(User).filter(User.username == user.identifier).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login credentials.")

    if not verify_hash(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Incorrect password.")
    
    access_token, max_age = create_access_token(existing_user.email)
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=max_age,
        httponly=True,
        samesite="lax",
        secure=True,
    )

    return {
        "user": existing_user,
        "message": "Successfully Logged In",
        "access_token": access_token,
        "token_type": "bearer",
    }