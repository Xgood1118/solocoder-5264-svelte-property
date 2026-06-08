from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional, List


class BillPaymentOut(BaseModel):
    id: int
    bill_id: int
    amount: float
    payment_method: Optional[str] = None
    paid_at: Optional[datetime] = None
    transaction_id: Optional[str] = None
    note: Optional[str] = ""
    created_at: datetime

    class Config:
        from_attributes = True


class BillOut(BaseModel):
    id: int
    contract_id: int
    bill_type: str
    period_start: date
    period_end: date
    due_date: date
    base_amount: float
    late_fee: float
    total_amount: float
    paid_amount: float
    status: str
    note: str
    created_at: datetime
    updated_at: datetime
    payments: List[BillPaymentOut] = []

    class Config:
        from_attributes = True


class BillPaymentCreate(BaseModel):
    amount: float
    payment_method: Optional[str] = "mock"
    transaction_id: Optional[str] = None
    note: Optional[str] = ""


class BillGenerateRequest(BaseModel):
    target_date: Optional[date] = None
