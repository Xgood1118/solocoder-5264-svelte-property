from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from ..database import get_db
from ..models import Property
from ..schemas import PropertyCreate, PropertyUpdate, PropertyOut

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("", response_model=List[PropertyOut])
async def list_properties(
    skip: int = 0,
    limit: int = 100,
    is_rented: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Property)
    if is_rented is not None:
        query = query.where(Property.is_rented == is_rented)
    query = query.order_by(desc(Property.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=PropertyOut)
async def create_property(
    data: PropertyCreate,
    db: AsyncSession = Depends(get_db),
):
    property_obj = Property(**data.model_dump())
    db.add(property_obj)
    await db.commit()
    await db.refresh(property_obj)
    return property_obj


@router.get("/{property_id}", response_model=PropertyOut)
async def get_property(
    property_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalar_one_or_none()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_obj


@router.put("/{property_id}", response_model=PropertyOut)
async def update_property(
    property_id: int,
    data: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalar_one_or_none()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(property_obj, key, value)
    
    await db.commit()
    await db.refresh(property_obj)
    return property_obj


@router.delete("/{property_id}")
async def delete_property(
    property_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Property).where(Property.id == property_id)
    )
    property_obj = result.scalar_one_or_none()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    await db.delete(property_obj)
    await db.commit()
    return {"message": "Property deleted successfully"}
