from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from typing import List

from ..database import get_db
from ..models import RenewalRequest, RenewalStatus, Contract
from ..schemas import RenewalRequestCreate, RenewalRequestOut, RenewalReview
from ..services import RenewalService

router = APIRouter(prefix="/renewals", tags=["renewals"])


@router.get("", response_model=List[RenewalRequestOut])
async def list_renewals(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    contract_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(RenewalRequest)
    if status:
        query = query.where(RenewalRequest.status == status)
    if contract_id:
        query = query.where(RenewalRequest.contract_id == contract_id)
    query = query.order_by(desc(RenewalRequest.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/contract/{contract_id}", response_model=RenewalRequestOut)
async def create_renewal_request(
    contract_id: int,
    data: RenewalRequestCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        request = await RenewalService.create_renewal_request(
            db=db,
            contract_id=contract_id,
            new_start_date=data.new_start_date,
            new_end_date=data.new_end_date,
            new_monthly_rent=data.new_monthly_rent,
            new_deposit=data.new_deposit,
            new_payment_cycle=data.new_payment_cycle,
            tenant_note=data.tenant_note,
        )
        return request
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{request_id}", response_model=RenewalRequestOut)
async def get_renewal(
    request_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(RenewalRequest).where(RenewalRequest.id == request_id)
    )
    request = result.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404, detail="Renewal request not found")
    return request


@router.post("/{request_id}/approve")
async def approve_renewal(
    request_id: int,
    data: RenewalReview | None = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        note = data.landlord_note if data else ""
        request, new_contract = await RenewalService.approve_renewal(
            db=db,
            request_id=request_id,
            landlord_note=note,
        )
        return {
            "request": request,
            "new_contract": new_contract,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{request_id}/reject", response_model=RenewalRequestOut)
async def reject_renewal(
    request_id: int,
    data: RenewalReview | None = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        note = data.landlord_note if data else ""
        request = await RenewalService.reject_renewal(
            db=db,
            request_id=request_id,
            landlord_note=note,
        )
        return request
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/check/{contract_id}")
async def check_renewal_availability(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    available = RenewalService.is_renewal_available(contract)
    
    return {
        "contract_id": contract_id,
        "renewal_available": available,
        "end_date": contract.end_date,
    }
