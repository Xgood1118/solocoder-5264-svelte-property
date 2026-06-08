from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class RenewalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class RenewalRequest(Base):
    __tablename__ = "renewal_requests"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    
    new_start_date = Column(Date, nullable=False)
    new_end_date = Column(Date, nullable=False)
    new_monthly_rent = Column(Float, nullable=False)
    new_deposit = Column(Float, default=0.0)
    new_payment_cycle = Column(String(20))
    
    tenant_note = Column(Text, default="")
    landlord_note = Column(Text, default="")
    
    status = Column(String(20), default=RenewalStatus.PENDING.value)
    
    submitted_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contract = relationship("Contract", back_populates="renewal_requests")
