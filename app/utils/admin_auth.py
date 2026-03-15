from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.utils.auth import get_current_user
from app.models.user_model import User

def get_admin_user(user = Depends(get_current_user)):

    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user["user_id"]).first()

    if db_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return db_user