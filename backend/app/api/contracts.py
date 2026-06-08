from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from ..database import get_db
from ..models import Contract, Property, Tenant, ContractStatus
from ..schemas import ContractCreate, ContractUpdate, ContractOut

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("", response_model=List[ContractOut])
async def list_contracts(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    property_id: int | None = None,
    tenant_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Contract)
    if status:
        query = query.where(Contract.status == status)
    if property_id:
        query = query.where(Contract.property_id == property_id)
    if tenant_id:
        query = query.where(Contract.tenant_id == tenant_id)
    query = query.order_by(desc(Contract.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", response_model=ContractOut)
async def create_contract(
    data: ContractCreate,
    db: AsyncSession = Depends(get_db),
):
    prop_result = await db.execute(
        select(Property).where(Property.id == data.property_id)
    )
    if not prop_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Property not found")
    
    tenant_result = await db.execute(
        select(Tenant).where(Tenant.id == data.tenant_id)
    )
    if not tenant_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    if data.end_date <= data.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    contract = Contract(**data.model_dump())
    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    
    if contract.status == ContractStatus.ACTIVE.value:
        prop = prop_result.scalar_one()
        prop.is_rented = True
        await db.commit()
    
    return contract


@router.get("/{contract_id}", response_model=ContractOut)
async def get_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.put("/{contract_id}", response_model=ContractOut)
async def update_contract(
    contract_id: int,
    data: ContractUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contract, key, value)
    
    await db.commit()
    await db.refresh(contract)
    return contract


@router.delete("/{contract_id}")
async def delete_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    await db.delete(contract)
    await db.commit()
    return {"message": "Contract deleted successfully"}


@router.post("/{contract_id}/terminate", response_model=ContractOut)
async def terminate_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    contract.status = ContractStatus.TERMINATED.value
    
    prop_result = await db.execute(
        select(Property).where(Property.id == contract.property_id)
    )
    prop = prop_result.scalar_one_or_none()
    if prop:
        active_contracts = await db.execute(
            select(Contract).where(
                Contract.property_id == prop.id,
                Contract.status == ContractStatus.ACTIVE.value,
                Contract.id != contract_id,
            )
        )
        if not active_contracts.scalars().first():
            prop.is_rented = False
    
    await db.commit()
    await db.refresh(contract)
    return contract
