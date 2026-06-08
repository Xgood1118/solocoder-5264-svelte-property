from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional


class ContractBase(BaseModel):
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    monthly_rent: float
    deposit: Optional[float] = 0.0
    payment_cycle: Optional[str] = "monthly"
    rent_due_day: Optional[int] = 1
    renewal_option: Optional[bool] = True
    note: Optional[str] = ""


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    property_id: Optional[int] = None
    tenant_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    monthly_rent: Optional[float] = None
    deposit: Optional[float] = None
    payment_cycle: Optional[str] = None
    rent_due_day: Optional[int] = None
    renewal_option: Optional[bool] = None
    status: Optional[str] = None
    note: Optional[str] = None


class ContractOut(BaseModel):
    id: int
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    monthly_rent: float
    deposit: float
    payment_cycle: str
    rent_due_day: int
    renewal_option: bool
    status: str
    note: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
