from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from src.database.db import Base

class ComplianceEvent(Base):
    __tablename__ = "compliance_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String, index=True)
    old_status = Column(String)
    new_status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
