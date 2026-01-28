from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import approve_request, get_db
from src.auth import review_auth

app = APIRouter()

@app.post("/approve/{request_id}")
def approve(request_id: str, edited_output: str, user=Depends(review_auth), db: Session = Depends(get_db)):
    approve_request(db, request_id, edited_output)
    return {"status": "APPROVED"}