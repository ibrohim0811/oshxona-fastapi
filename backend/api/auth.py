from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.auth import RegisterSchema, LoginSchema, TokenSchema, UserOutSchema
from backend.crud.user import get_user_by_email, create_user
from backend.core.security import hash_password, verify_password, create_access_token
from backend.core.deps import get_current_user
from backend.models import Customer

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserOutSchema, status_code=status.HTTP_201_CREATED)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    # 1. Email band emasligini tekshirish
    if get_user_by_email(data.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email allaqachon ro'yxatdan o'tgan",
        )

    # 2. Parolni hashlash va foydalanuvchini yaratish
    user = create_user(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=hash_password(data.password),
        db=db,
    )
    return user


@router.post("/login", response_model=TokenSchema)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(data.email, db)

    # user yo'q YOKI parol noto'g'ri — bir xil 401 (user enumeration'dan himoya)
    if not user or not user.hashed_password or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri",
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOutSchema)
def me(current_user: Customer = Depends(get_current_user)):
    """Joriy (tokenli) foydalanuvchi ma'lumotlari."""
    return current_user
