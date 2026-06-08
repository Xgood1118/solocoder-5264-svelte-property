from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import json

from ..database import get_db
from ..models import CheckoutSettlement, Contract
from ..schemas import CheckoutSettlementCreate, CheckoutSettlementOut, DeductionItem
from ..services import CheckoutService

router = APIRouter(prefix="/checkout", tags=["checkout"])


@router.post("/contract/{contract_id}", response_model=CheckoutSettlementOut)
async def create_checkout_settlement(
    contract_id: int,
    data: CheckoutSettlementCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        settlement = await CheckoutService.create_settlement(
            db=db,
            contract_id=contract_id,
            checkout_date=data.checkout_date,
            cleaning_fee=data.cleaning_fee,
            repair_fee=data.repair_fee,
            note=data.note,
        )
        
        deductions = []
        try:
            raw = json.loads(settlement.deductions_detail) if settlement.deductions_detail else []
            for d in raw:
                deductions.append(DeductionItem(**d))
        except (json.JSONDecodeError, TypeError):
            pass
        
        result = CheckoutSettlementOut(
            id=settlement.id,
            contract_id=settlement.contract_id,
            checkout_date=settlement.checkout_date,
            is_early_termination=settlement.is_early_termination == "true",
            original_deposit=settlement.original_deposit,
            cleaning_fee=settlement.cleaning_fee,
            repair_fee=settlement.repair_fee,
            unpaid_rent=settlement.unpaid_rent,
            late_fees=settlement.late_fees,
            early_termination_penalty=settlement.early_termination_penalty,
            deductions=deductions,
            total_deductions=settlement.total_deductions,
            refund_amount=settlement.refund_amount,
            note=settlement.note,
            settled_at=settlement.settled_at,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contract/{contract_id}", response_model=CheckoutSettlementOut)
async def get_checkout_settlement(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CheckoutSettlement).where(CheckoutSettlement.contract_id == contract_id)
    )
    settlement = result.scalar_one_or_none()
    if not settlement:
        raise HTTPException(status_code=404, detail="Checkout settlement not found")
    
    deductions = []
    try:
        raw = json.loads(settlement.deductions_detail) if settlement.deductions_detail else []
        for d in raw:
            deductions.append(DeductionItem(**d))
    except (json.JSONDecodeError, TypeError):
        pass
    
    result_obj = CheckoutSettlementOut(
        id=settlement.id,
        contract_id=settlement.contract_id,
        checkout_date=settlement.checkout_date,
        is_early_termination=settlement.is_early_termination == "true",
        original_deposit=settlement.original_deposit,
        cleaning_fee=settlement.cleaning_fee,
        repair_fee=settlement.repair_fee,
        unpaid_rent=settlement.unpaid_rent,
        late_fees=settlement.late_fees,
        early_termination_penalty=settlement.early_termination_penalty,
        deductions=deductions,
        total_deductions=settlement.total_deductions,
        refund_amount=settlement.refund_amount,
        note=settlement.note,
        settled_at=settlement.settled_at,
    )
    return result_obj
