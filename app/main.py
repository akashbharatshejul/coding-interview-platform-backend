from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.database import engine, Base, SessionLocal
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password
from app.utils.security import verify_password, create_access_token
from app.schemas.user_schema import UserLogin

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Coding Interview Platform Backend"}


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid password"}

    token = create_access_token({"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }