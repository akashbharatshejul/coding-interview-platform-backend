from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    difficulty = Column(String)