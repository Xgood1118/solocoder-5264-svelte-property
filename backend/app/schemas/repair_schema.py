from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional


class RepairBase(BaseModel):
    property_id: int
    tenant_id: Optional[int] = None
    contract_id: Optional[int] = None
    title: str
    description: str
    urgency: Optional[str] = "medium"
    photo_urls: Optional[str] = ""


class RepairCreate(RepairBase):
    pass


class RepairUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    urgency: Optional[str] = None
    photo_urls: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    cost_estimate: Optional[float] = None
    actual_cost: Optional[float] = None
    cost_responsibility: Optional[str] = None
    landlord_note: Optional[str] = None
    tenant_note: Optional[str] = None


class RepairOut(BaseModel):
    id: int
    property_id: int
    tenant_id: Optional[int] = None
    contract_id: Optional[int] = None
    title: str
    description: str
    urgency: str
    photo_urls: str
    status: str
    assigned_to: Optional[str] = None
    cost_estimate: float
    actual_cost: float
    cost_responsibility: Optional[str] = None
    landlord_note: str
    tenant_note: str
    submitted_at: datetime
    accepted_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    accepted_by_tenant_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RepairCostAssign(BaseModel):
    damage_cause: str
    actual_cost: float
