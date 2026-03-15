from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.database import engine, Base, SessionLocal
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password
from app.utils.security import verify_password, create_access_token
from app.schemas.user_schema import UserLogin
from app.models.question_model import Question
from app.schemas.question_schema import QuestionCreate
from app.models import question_model
from app.models.submission_model import Submission
from app.schemas.submission_schema import SubmissionCreate
from app.models import submission_model
from app.utils.auth import get_current_user
from app.services.judge_service import run_code
from sqlalchemy import func
from app.utils.admin_auth import get_admin_user


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


@app.post("/questions")
def add_question(
    question: QuestionCreate,
    admin = Depends(get_admin_user),
    db: Session = Depends(get_db)
):

    new_question = Question(
        title=question.title,
        description=question.description,
        difficulty=question.difficulty
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {"message": "Question added"}

@app.get("/questions")
def get_questions(db: Session = Depends(get_db)):

    questions = db.query(Question).all()

    return questions

@app.get("/questions/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        return {"error": "Question not found"}

    return question

@app.post("/submit")
def submit_code(
    submission: SubmissionCreate,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    test_cases = [
        {"input": "1 2", "output": "3"},
        {"input": "5 7", "output": "12"},
        {"input": "10 20", "output": "30"}
    ]

    status = "Accepted"

    for test in test_cases:
        output = run_code(submission.code, test["input"])

        if output != test["output"]:
            status = "Wrong Answer"
            break

    new_submission = Submission(
        user_id=user["user_id"],
        question_id=submission.question_id,
        code=submission.code,
        status=status
    )

    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return {"status": status}

@app.get("/submissions")
def get_submissions(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    submissions = db.query(Submission).filter(
        Submission.user_id == user["user_id"]
    ).all()

    return submissions

@app.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):

    leaderboard = (
        db.query(
            User.username,
            func.count(Submission.id).label("score")
        )
        .join(Submission, Submission.user_id == User.id)
        .filter(Submission.status == "Accepted")
        .group_by(User.username)
        .order_by(func.count(Submission.id).desc())
        .all()
    )

    result = []

    for row in leaderboard:
        result.append({
            "username": row.username,
            "score": row.score
        })

    return result

@app.get("/profile")
def get_profile(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(User.id == user["user_id"]).first()

    return {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email
    }

@app.get("/my-submissions")
def my_submissions(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    submissions = db.query(Submission).filter(
        Submission.user_id == user["user_id"]
    ).all()

    result = []

    for sub in submissions:
        result.append({
            "question_id": sub.question_id,
            "status": sub.status
        })

    return result

@app.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    admin = Depends(get_admin_user),
    db: Session = Depends(get_db)
):

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        return {"error": "Question not found"}

    db.delete(question)
    db.commit()

    return {"message": "Question deleted"}