from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database import get_request_by_id

app = APIRouter()

@app.get("/result/{request_id}")
def get_result(request_id: str, db: Session = Depends(get_db)):
    record = get_request_by_id(db, request_id)

    if not record:
        raise HTTPException(status_code = 404, detail = "Request Not Found")
    
    return {
        "request_id": record.request_id,
        "status": record.status,
        "final_output": record.final_output if record.status == "APPROVED" else None
    }