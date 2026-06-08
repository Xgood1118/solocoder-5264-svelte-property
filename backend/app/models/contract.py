from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class PaymentCycle(str, enum.Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class ContractStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    monthly_rent = Column(Float, nullable=False)
    deposit = Column(Float, default=0.0)
    payment_cycle = Column(String(20), default=PaymentCycle.MONTHLY.value)
    
    rent_due_day = Column(Integer, default=1)
    renewal_option = Column(Boolean, default=True)
    status = Column(String(20), default=ContractStatus.ACTIVE.value)
    
    note = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property = relationship("Property", back_populates="contracts")
    tenant = relationship("Tenant", back_populates="contracts")
    bills = relationship("Bill", back_populates="contract")
    renewal_requests = relationship("RenewalRequest", back_populates="contract")
    checkout_settlement = relationship("CheckoutSettlement", back_populates="contract", uselist=False)
