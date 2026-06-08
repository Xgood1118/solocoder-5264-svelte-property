from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class BillStatus(str, enum.Enum):
    UNPAID = "unpaid"
    PARTIAL = "partial"
    PAID = "paid"
    OVERDUE = "overdue"


class BillType(str, enum.Enum):
    RENT = "rent"
    UTILITY = "utility"
    OTHER = "other"


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    
    bill_type = Column(String(20), default=BillType.RENT.value)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    base_amount = Column(Float, default=0.0)
    late_fee = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    paid_amount = Column(Float, default=0.0)
    
    status = Column(String(20), default=BillStatus.UNPAID.value)
    note = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contract = relationship("Contract", back_populates="bills")
    payments = relationship("BillPayment", back_populates="bill")


class BillPayment(Base):
    __tablename__ = "bill_payments"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50))
    paid_at = Column(DateTime, default=datetime.utcnow)
    transaction_id = Column(String(200))
    note = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    bill = relationship("Bill", back_populates="payments")
