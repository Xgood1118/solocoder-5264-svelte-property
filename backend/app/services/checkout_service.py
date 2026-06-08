from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ..models import Contract, CheckoutSettlement, Bill, BillStatus, ContractStatus
from ..config import settings


class CheckoutService:
    @staticmethod
    def calculate_early_termination_penalty(
        contract: Contract,
        checkout_date: date,
    ) -> float:
        if checkout_date >= contract.end_date:
            return 0.0
        
        remaining_months = 0
        current = checkout_date
        while current < contract.end_date:
            remaining_months += 1
            current = current + relativedelta(months=1)
        
        penalty = remaining_months * contract.monthly_rent * settings.early_termination_penalty_rate
        return round(penalty, 2)

    @classmethod
    async def create_settlement(
        cls,
        db: AsyncSession,
        contract_id: int,
        checkout_date: date,
        cleaning_fee: float = 0.0,
        repair_fee: float = 0.0,
        note: str = "",
    ) -> CheckoutSettlement:
        result = await db.execute(
            select(Contract).where(Contract.id == contract_id)
        )
        contract = result.scalar_one_or_none()
        if not contract:
            raise ValueError(f"Contract {contract_id} not found")
        
        existing = await db.execute(
            select(CheckoutSettlement).where(CheckoutSettlement.contract_id == contract_id)
        )
        if existing.scalar_one_or_none():
            raise ValueError("该合同已有退租结算")
        
        bills_result = await db.execute(
            select(Bill).where(
                and_(
                    Bill.contract_id == contract_id,
                    Bill.bill_type == "rent",
                    Bill.period_end <= checkout_date,
                )
            ).order_by(Bill.period_start)
        )
        bills = bills_result.scalars().all()
        
        unpaid_rent = 0.0
        total_late_fees = 0.0
        for bill in bills:
            remaining = bill.total_amount - bill.paid_amount
            if remaining > 0:
                unpaid_rent += bill.base_amount
                total_late_fees += bill.late_fee
        
        is_early = checkout_date < contract.end_date
        early_penalty = cls.calculate_early_termination_penalty(contract, checkout_date) if is_early else 0.0
        
        deductions = []
        
        if cleaning_fee > 0:
            deductions.append({"type": "cleaning", "name": "清洁费", "amount": cleaning_fee})
        
        if repair_fee > 0:
            deductions.append({"type": "repair", "name": "维修费", "amount": repair_fee})
        
        if unpaid_rent > 0:
            deductions.append({"type": "unpaid_rent", "name": "欠缴房租", "amount": round(unpaid_rent, 2)})
        
        if total_late_fees > 0:
            deductions.append({"type": "late_fee", "name": "滞纳金", "amount": round(total_late_fees, 2)})
        
        if early_penalty > 0:
            deductions.append({"type": "early_termination", "name": "提前解约违约金", "amount": early_penalty})
        
        total_deductions = sum(d["amount"] for d in deductions)
        refund_amount = max(0.0, contract.deposit - total_deductions)
        
        import json
        settlement = CheckoutSettlement(
            contract_id=contract_id,
            checkout_date=checkout_date,
            is_early_termination="true" if is_early else "false",
            original_deposit=contract.deposit,
            cleaning_fee=cleaning_fee,
            repair_fee=repair_fee,
            unpaid_rent=round(unpaid_rent, 2),
            late_fees=round(total_late_fees, 2),
            early_termination_penalty=early_penalty,
            deductions_detail=json.dumps(deductions, ensure_ascii=False),
            total_deductions=round(total_deductions, 2),
            refund_amount=round(refund_amount, 2),
            note=note,
        )
        
        contract.status = ContractStatus.TERMINATED.value if is_early else ContractStatus.EXPIRED.value
        
        db.add(settlement)
        await db.commit()
        await db.refresh(settlement)
        
        return settlement

    @staticmethod
    def format_settlement_detail(settlement: CheckoutSettlement) -> dict:
        import json
        deductions = json.loads(settlement.deductions_detail) if settlement.deductions_detail else []
        
        return {
            "id": settlement.id,
            "contract_id": settlement.contract_id,
            "checkout_date": settlement.checkout_date.isoformat(),
            "is_early_termination": settlement.is_early_termination == "true",
            "original_deposit": settlement.original_deposit,
            "deductions": deductions,
            "total_deductions": settlement.total_deductions,
            "refund_amount": settlement.refund_amount,
            "note": settlement.note,
            "settled_at": settlement.settled_at.isoformat() if settlement.settled_at else None,
        }
