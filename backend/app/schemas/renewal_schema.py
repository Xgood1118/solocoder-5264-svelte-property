from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional


class RenewalRequestBase(BaseModel):
    contract_id: int
    new_start_date: date
    new_end_date: date
    new_monthly_rent: float
    new_deposit: Optional[float] = 0.0
    new_payment_cycle: Optional[str] = None
    tenant_note: Optional[str] = ""


class RenewalRequestCreate(BaseModel):
    new_start_date: date
    new_end_date: date
    new_monthly_rent: float
    new_deposit: Optional[float] = 0.0
    new_payment_cycle: Optional[str] = None
    tenant_note: Optional[str] = ""


class RenewalReview(BaseModel):
    landlord_note: Optional[str] = ""


class RenewalRequestOut(BaseModel):
    id: int
    contract_id: int
    new_start_date: date
    new_end_date: date
    new_monthly_rent: float
    new_deposit: float
    new_payment_cycle: Optional[str] = None
    tenant_note: str
    landlord_note: str
    status: str
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
