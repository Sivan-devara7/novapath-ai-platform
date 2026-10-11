from typing import Optional
from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.db_models import User

DEMO_USER_ID = "usr-aarav-sharma"

def get_current_user(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
) -> User:
    """
    Resolves the current authenticated user from the Authorization Bearer header.
    Falls back gracefully to the pre-seeded demo user if unauthenticated.
    """
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1].strip()
        user_id = None
        if token.startswith("jwt-token-"):
            user_id = token[len("jwt-token-"):]
        else:
            user_id = token

        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return user

    # Fallback to demo user
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        user = db.query(User).first()

    if not user:
        raise HTTPException(status_code=404, detail="No active user found")

    return user
