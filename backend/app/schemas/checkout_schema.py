from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional, List, Any


class CheckoutSettlementCreate(BaseModel):
    checkout_date: date
    cleaning_fee: Optional[float] = 0.0
    repair_fee: Optional[float] = 0.0
    note: Optional[str] = ""


class DeductionItem(BaseModel):
    type: str
    name: str
    amount: float


class CheckoutSettlementOut(BaseModel):
    id: int
    contract_id: int
    checkout_date: date
    is_early_termination: bool
    original_deposit: float
    cleaning_fee: float
    repair_fee: float
    unpaid_rent: float
    late_fees: float
    early_termination_penalty: float
    deductions: List[DeductionItem] = []
    total_deductions: float
    refund_amount: float
    note: str
    settled_at: Optional[datetime] = None

    class Config:
        from_attributes = True
