from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    question_id = Column(Integer)
    code = Column(String)
    status = Column(String)