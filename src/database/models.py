from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime
from src.database.db import Base

class ComplianceRequest(Base):
    __tablename__ = "compliance_requests"

    request_id = Column(String, primary_key=True, index=True)
    user_input = Column(Text)
    ai_draft = Column(Text)
    final_output = Column(Text, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
