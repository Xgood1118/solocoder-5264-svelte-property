from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from ..database import get_db
from ..models import Tenant
from ..schemas import TenantCreate, TenantUpdate, TenantOut
from ..schemas.tenant_schema import mask_phone, mask_id_card

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get("", response_model=List[TenantOut])
async def list_tenants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    query = select(Tenant).order_by(desc(Tenant.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    tenants = result.scalars().all()
    
    masked = []
    for t in tenants:
        obj = TenantOut.model_validate(t, from_attributes=True)
        obj.phone = mask_phone(obj.phone) if obj.phone else obj.phone
        if obj.id_card:
            obj.id_card = mask_id_card(obj.id_card)
        if obj.emergency_phone:
            obj.emergency_phone = mask_phone(obj.emergency_phone)
        masked.append(obj)
    
    return masked


@router.post("", response_model=TenantOut)
async def create_tenant(
    data: TenantCreate,
    db: AsyncSession = Depends(get_db),
):
    tenant = Tenant(**data.model_dump())
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    
    obj = TenantOut.model_validate(tenant, from_attributes=True)
    obj.phone = mask_phone(obj.phone) if obj.phone else obj.phone
    if obj.id_card:
        obj.id_card = mask_id_card(obj.id_card)
    if obj.emergency_phone:
        obj.emergency_phone = mask_phone(obj.emergency_phone)
    return obj


@router.get("/{tenant_id}", response_model=TenantOut)
async def get_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Tenant).where(Tenant.id == tenant_id)
    )
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    obj = TenantOut.model_validate(tenant, from_attributes=True)
    obj.phone = mask_phone(obj.phone) if obj.phone else obj.phone
    if obj.id_card:
        obj.id_card = mask_id_card(obj.id_card)
    if obj.emergency_phone:
        obj.emergency_phone = mask_phone(obj.emergency_phone)
    return obj


@router.put("/{tenant_id}", response_model=TenantOut)
async def update_tenant(
    tenant_id: int,
    data: TenantUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Tenant).where(Tenant.id == tenant_id)
    )
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tenant, key, value)
    
    await db.commit()
    await db.refresh(tenant)
    
    obj = TenantOut.model_validate(tenant, from_attributes=True)
    obj.phone = mask_phone(obj.phone) if obj.phone else obj.phone
    if obj.id_card:
        obj.id_card = mask_id_card(obj.id_card)
    if obj.emergency_phone:
        obj.emergency_phone = mask_phone(obj.emergency_phone)
    return obj


@router.delete("/{tenant_id}")
async def delete_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Tenant).where(Tenant.id == tenant_id)
    )
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    await db.delete(tenant)
    await db.commit()
    return {"message": "Tenant deleted successfully"}
