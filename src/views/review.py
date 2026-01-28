from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db, create_request
from src.schema.pending_review import ReviewRequest 
from src.engine import run_compliance_review
from src.shared.utils import detect_intent_conflict
import uuid

app = APIRouter()

@app.post("/review")
def review(request: ReviewRequest, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())

    create_request(db, request_id, request.input)

    intent_override = detect_intent_conflict(request.input)

    run_compliance_review(request.input, request_id, intent_override)

    return {
        "request_id": request_id,
        "status": "UNDER_REVIEW"
    }   