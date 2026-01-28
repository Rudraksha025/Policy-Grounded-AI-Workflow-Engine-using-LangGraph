from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db, get_pending_human_reviews
from src.auth import review_auth

app = APIRouter()

@app.get("/pending_reviews")
def list_pending_reviews(user = Depends(review_auth), db: Session = Depends(get_db)):
    records = get_pending_human_reviews(db)

    return [
        {
            "request_id": r.request_id,
            "user_input": r.user_input,
            "ai_draft": r.ai_draft,
            "created_at": r.created_at
        } 
        for r in records
    ]