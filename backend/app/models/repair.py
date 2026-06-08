from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class RepairStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ACCEPTED_BY_TENANT = "accepted_by_tenant"


class RepairUrgency(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"


class RepairCostResponsibility(str, enum.Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"
    NEGOTIATED = "negotiated"


class Repair(Base):
    __tablename__ = "repairs"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    urgency = Column(String(20), default=RepairUrgency.MEDIUM.value)
    photo_urls = Column(Text, default="")
    
    status = Column(String(30), default=RepairStatus.SUBMITTED.value)
    
    assigned_to = Column(String(100))
    cost_estimate = Column(Float, default=0.0)
    actual_cost = Column(Float, default=0.0)
    cost_responsibility = Column(String(20))
    
    landlord_note = Column(Text, default="")
    tenant_note = Column(Text, default="")
    
    submitted_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    accepted_by_tenant_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property = relationship("Property", back_populates="repairs")
