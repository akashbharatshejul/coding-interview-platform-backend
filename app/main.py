from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Coding Interview Platform Backend"}