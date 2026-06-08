import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


def mask_phone(phone: str) -> str:
    if not phone or len(phone) < 7:
        return phone
    return phone[:3] + "****" + phone[-4:]


def mask_id_card(id_card: str) -> str:
    if not id_card or len(id_card) < 8:
        return id_card
    return id_card[:4] + "********" + id_card[-4:]


class TenantBase(BaseModel):
    name: str
    phone: str
    id_card: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = ""


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    id_card: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None


class TenantOut(BaseModel):
    id: int
    name: str
    phone: str
    id_card: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = ""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_masked(cls, tenant) -> "TenantOut":
        obj = cls.model_validate(tenant, from_attributes=True)
        obj.phone = mask_phone(obj.phone) if obj.phone else obj.phone
        obj.id_card = mask_id_card(obj.id_card) if obj.id_card else obj.id_card
        if obj.emergency_phone:
            obj.emergency_phone = mask_phone(obj.emergency_phone)
        return obj
