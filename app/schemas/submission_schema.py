from pydantic import BaseModel

class SubmissionCreate(BaseModel):
    question_id: int
    code: str