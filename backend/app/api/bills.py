from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from typing import List
from datetime import date

from ..database import get_db
from ..models import Bill, BillPayment, Contract, BillStatus
from ..schemas import BillOut, BillPaymentCreate, BillGenerateRequest
from ..services import BillService

router = APIRouter(prefix="/bills", tags=["bills"])


@router.get("", response_model=List[BillOut])
async def list_bills(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    contract_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Bill)
    if status:
        query = query.where(Bill.status == status)
    if contract_id:
        query = query.where(Bill.contract_id == contract_id)
    query = query.order_by(desc(Bill.due_date)).offset(skip).limit(limit)
    result = await db.execute(query)
    bills = result.scalars().all()
    return bills


@router.get("/{bill_id}", response_model=BillOut)
async def get_bill(
    bill_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Bill).where(Bill.id == bill_id)
    )
    bill = result.scalar_one_or_none()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@router.post("/{bill_id}/pay", response_model=BillOut)
async def pay_bill(
    bill_id: int,
    data: BillPaymentCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        bill = await BillService.record_payment(
            db=db,
            bill_id=bill_id,
            amount=data.amount,
            payment_method=data.payment_method,
            transaction_id=data.transaction_id,
            note=data.note,
        )
        return bill
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate")
async def generate_bills(
    data: BillGenerateRequest | None = None,
    db: AsyncSession = Depends(get_db),
):
    target_date = data.target_date if data else None
    bills = await BillService.generate_monthly_bills(db, target_date)
    return {"generated_count": len(bills), "bills": bills}


@router.post("/check-overdue")
async def check_overdue_bills(
    db: AsyncSession = Depends(get_db),
):
    count = await BillService.update_overdue_bills(db)
    return {"overdue_count": count}


@router.get("/{bill_id}/payments", response_model=List)
async def list_bill_payments(
    bill_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(BillPayment).where(BillPayment.bill_id == bill_id).order_by(desc(BillPayment.paid_at))
    )
    return result.scalars().all()
