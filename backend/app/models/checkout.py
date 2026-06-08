from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import json


class CheckoutSettlement(Base):
    __tablename__ = "checkout_settlements"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False, unique=True)
    
    checkout_date = Column(Date, nullable=False)
    is_early_termination = Column(String(10), default="false")
    
    original_deposit = Column(Float, default=0.0)
    
    cleaning_fee = Column(Float, default=0.0)
    repair_fee = Column(Float, default=0.0)
    unpaid_rent = Column(Float, default=0.0)
    late_fees = Column(Float, default=0.0)
    early_termination_penalty = Column(Float, default=0.0)
    
    deductions_detail = Column(Text, default="[]")
    
    total_deductions = Column(Float, default=0.0)
    refund_amount = Column(Float, default=0.0)
    
    note = Column(Text, default="")
    settled_at = Column(DateTime, default=datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contract = relationship("Contract", back_populates="checkout_settlement")
    
    @property
    def deductions_list(self):
        try:
            return json.loads(self.deductions_detail) if self.deductions_detail else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    @deductions_list.setter
    def deductions_list(self, value):
        self.deductions_detail = json.dumps(value, ensure_ascii=False)
