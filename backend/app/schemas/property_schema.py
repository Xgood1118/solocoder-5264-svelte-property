from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Optional, List


class PropertyBase(BaseModel):
    address: str
    house_type: Optional[str] = None
    area: Optional[float] = None
    floor: Optional[str] = None
    decoration_status: Optional[str] = None
    photo_urls: Optional[str] = ""
    is_rented: Optional[bool] = False
    note: Optional[str] = ""


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    address: Optional[str] = None
    house_type: Optional[str] = None
    area: Optional[float] = None
    floor: Optional[str] = None
    decoration_status: Optional[str] = None
    photo_urls: Optional[str] = None
    is_rented: Optional[bool] = None
    note: Optional[str] = None


class PropertyOut(PropertyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
