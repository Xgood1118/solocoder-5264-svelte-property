from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import Repair, RepairStatus, Property
from ..schemas import RepairCreate, RepairUpdate, RepairOut, RepairCostAssign
from ..services import RepairService

router = APIRouter(prefix="/repairs", tags=["repairs"])


@router.get("", response_model=List[RepairOut])
async def list_repairs(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    property_id: int | None = None,
    urgency: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Repair)
    if status:
        query = query.where(Repair.status == status)
    if property_id:
        query = query.where(Repair.property_id == property_id)
    if urgency:
        query = query.where(Repair.urgency == urgency)
    query = query.order_by(desc(Repair.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=RepairOut)
async def create_repair(
    data: RepairCreate,
    db: AsyncSession = Depends(get_db),
):
    prop_result = await db.execute(
        select(Property).where(Property.id == data.property_id)
    )
    if not prop_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Property not found")
    
    repair = Repair(**data.model_dump())
    db.add(repair)
    await db.commit()
    await db.refresh(repair)
    return repair


@router.get("/{repair_id}", response_model=RepairOut)
async def get_repair(
    repair_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repair).where(Repair.id == repair_id)
    )
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    return repair


@router.put("/{repair_id}", response_model=RepairOut)
async def update_repair(
    repair_id: int,
    data: RepairUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repair).where(Repair.id == repair_id)
    )
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(repair, key, value)
    
    await db.commit()
    await db.refresh(repair)
    return repair


@router.post("/{repair_id}/accept", response_model=RepairOut)
async def accept_repair(
    repair_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repair).where(Repair.id == repair_id)
    )
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    repair.status = RepairStatus.ACCEPTED.value
    repair.accepted_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(repair)
    return repair


@router.post("/{repair_id}/start", response_model=RepairOut)
async def start_repair(
    repair_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repair).where(Repair.id == repair_id)
    )
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    repair.status = RepairStatus.IN_PROGRESS.value
    repair.started_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(repair)
    return repair


@router.post("/{repair_id}/complete", response_model=RepairOut)
async def complete_repair(
    repair_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repair).where(Repair.id == repair_id)
    )
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    repair.status = RepairStatus.COMPLETED.value
    repair.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(repair)
    return repair


@router.post("/{repair_id}/accept-by-tenant", response_model=RepairOut)
async def accept_by_tenant(
    repair_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repair).where(Repair.id == repair_id)
    )
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    repair.status = RepairStatus.ACCEPTED_BY_TENANT.value
    repair.accepted_by_tenant_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(repair)
    return repair


@router.post("/{repair_id}/assign-cost")
async def assign_repair_cost(
    repair_id: int,
    data: RepairCostAssign,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repair).where(Repair.id == repair_id)
    )
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    responsibility, description = RepairService.determine_cost_responsibility(
        data.damage_cause, data.actual_cost
    )
    
    repair.actual_cost = data.actual_cost
    repair.cost_responsibility = responsibility
    repair.landlord_note = description
    
    await db.commit()
    await db.refresh(repair)
    
    split = RepairService.split_cost(data.actual_cost, responsibility)
    
    return {
        "repair_id": repair_id,
        "responsibility": responsibility,
        "description": description,
        "tenant_cost": split["tenant"],
        "landlord_cost": split["landlord"],
    }


@router.delete("/{repair_id}")
async def delete_repair(
    repair_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repair).where(Repair.id == repair_id)
    )
    repair = result.scalar_one_or_none()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    
    await db.delete(repair)
    await db.commit()
    return {"message": "Repair deleted successfully"}
