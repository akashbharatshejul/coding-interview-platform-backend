from sqlalchemy import Column, Integer, String
from app.database.database import Base

class TestCase(Base):

    __tablename__ = "testcases"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer)
    input = Column(String)
    output = Column(String)