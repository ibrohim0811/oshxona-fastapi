from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.core.security import decode_access_token
from backend.models import Customer

# Swagger UI dagi "Authorize" tugmasi shu tokenUrl ga qarab ishlaydi
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Customer:
    """Authorization: Bearer <token> ni tekshirib, joriy foydalanuvchini qaytaradi."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Yaroqsiz yoki muddati o'tgan token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception

    user = db.query(Customer).filter(Customer.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user
