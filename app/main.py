from fastapi import FastAPI
from app.database.database import engine, Base
from app.models import user_model

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Coding Interview Platform Backend"}