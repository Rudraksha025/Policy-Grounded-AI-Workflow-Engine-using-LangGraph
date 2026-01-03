from fastapi import FastAPI
from pydantic import BaseModel
from main import run_compliance_review
from human_review import get_reviews, approve_review

app = FastAPI(title="Compliance AI Engine")

class ReviewRequest(BaseModel):
    input: str

@app.post("/review")
def review_text(data: ReviewRequest):
    return run_compliance_review(data.input)

@app.get("/reviews")
def list_pending_reviews():
    return get_reviews()

@app.post("/approve/{task_id}")
def approve(task_id: str, edited_output: str | None = None):
    return approve_review(task_id, edited_output)