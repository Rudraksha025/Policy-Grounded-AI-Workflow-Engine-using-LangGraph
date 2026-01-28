from sqlalchemy.orm import Session
from src.database.models import ComplianceRequest
from src.database.events import ComplianceEvent
from datetime import datetime, timedelta

def create_request(db: Session, request_id: str, user_input: str):
    record = ComplianceRequest(
        request_id=request_id,
        user_input=user_input,
        status="PENDING_AI"
    )
    db.add(record)
    db.commit()
    log_status_change(db, request_id, "NONE", "PENDING_AI")
    return record


def update_ai_draft(db: Session, request_id: str, ai_draft: str, new_status: str):
    record = db.query(ComplianceRequest).filter_by(request_id=request_id).first()
    old_status = record.status

    record.ai_draft = ai_draft
    record.status = new_status
    db.commit() 

    log_status_change(db, request_id, old_status, new_status)
    return record


def get_request_by_id(db: Session, request_id: str):
    return db.query(ComplianceRequest).filter_by(request_id=request_id).first()


def approve_request(db: Session, request_id: str, final_output: str):
    record = db.query(ComplianceRequest).filter_by(request_id=request_id).first()
    old_status = record.status

    record.final_output = final_output
    record.status = "APPROVED"
    db.commit()

    log_status_change(db, request_id, old_status, "APPROVED")
    return record


def get_pending_human_reviews(db: Session):
    return db.query(ComplianceRequest).filter_by(status="PENDING_HUMAN").all()


def log_status_change(db: Session, request_id: str, old_status: str, new_status: str):
    event = ComplianceEvent(
        request_id=request_id,
        old_status=old_status,
        new_status=new_status
    )
    db.add(event)
    db.commit()

def get_stale_pending_requests(db: Session, hours: int = 24):
    threshold = datetime.utcnow() - timedelta(hours=hours)
    return db.query(ComplianceRequest).filter(
        ComplianceRequest.status == "PENDING_HUMAN",
        ComplianceRequest.created_at < threshold
    ).all()