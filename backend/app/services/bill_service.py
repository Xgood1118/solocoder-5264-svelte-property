from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from ..models import Contract, Bill, BillPayment, BillStatus, ContractStatus
from ..config import settings


class BillService:
    @staticmethod
    def calculate_late_fee(due_date: date, pay_date: date, monthly_rent: float) -> float:
        if pay_date <= due_date:
            return 0.0
        days_overdue = (pay_date - due_date).days
        late_fee = days_overdue * monthly_rent * settings.late_fee_rate
        max_late_fee = monthly_rent * settings.max_late_fee_ratio
        return min(late_fee, max_late_fee)

    @staticmethod
    def get_bill_period(contract: Contract, reference_date: date) -> tuple[date, date]:
        cycle = contract.payment_cycle
        if cycle == "monthly":
            period_start = date(reference_date.year, reference_date.month, 1)
            period_end = period_start + relativedelta(months=1) - timedelta(days=1)
        elif cycle == "quarterly":
            quarter = (reference_date.month - 1) // 3
            period_start = date(reference_date.year, quarter * 3 + 1, 1)
            period_end = period_start + relativedelta(months=3) - timedelta(days=1)
        elif cycle == "yearly":
            period_start = date(reference_date.year, 1, 1)
            period_end = date(reference_date.year, 12, 31)
        else:
            period_start = date(reference_date.year, reference_date.month, 1)
            period_end = period_start + relativedelta(months=1) - timedelta(days=1)
        return period_start, period_end

    @staticmethod
    def get_cycle_months(payment_cycle: str) -> int:
        if payment_cycle == "monthly":
            return 1
        elif payment_cycle == "quarterly":
            return 3
        elif payment_cycle == "yearly":
            return 12
        return 1

    @classmethod
    async def generate_bills_for_contract(
        cls,
        db: AsyncSession,
        contract: Contract,
        target_date: date | None = None
    ) -> list[Bill]:
        if contract.status != ContractStatus.ACTIVE.value:
            return []
        
        if target_date is None:
            target_date = date.today()
        
        period_start, period_end = cls.get_bill_period(contract, target_date)
        
        if period_end < contract.start_date or period_start > contract.end_date:
            return []
        
        actual_start = max(period_start, contract.start_date)
        actual_end = min(period_end, contract.end_date)
        
        cycle_months = cls.get_cycle_months(contract.payment_cycle)
        base_amount = contract.monthly_rent * cycle_months
        
        due_date = date(period_start.year, period_start.month, contract.rent_due_day)
        
        existing = await db.execute(
            select(Bill).where(
                and_(
                    Bill.contract_id == contract.id,
                    Bill.bill_type == "rent",
                    Bill.period_start == period_start,
                    Bill.period_end == period_end,
                )
            )
        )
        if existing.scalar_one_or_none():
            return []
        
        bill = Bill(
            contract_id=contract.id,
            bill_type="rent",
            period_start=actual_start,
            period_end=actual_end,
            due_date=due_date,
            base_amount=base_amount,
            late_fee=0.0,
            total_amount=base_amount,
            paid_amount=0.0,
            status=BillStatus.UNPAID.value,
        )
        
        db.add(bill)
        await db.flush()
        return [bill]

    @classmethod
    async def generate_monthly_bills(cls, db: AsyncSession, target_date: date | None = None) -> list[Bill]:
        if target_date is None:
            target_date = date.today()
        
        result = await db.execute(
            select(Contract).where(
                and_(
                    Contract.status == ContractStatus.ACTIVE.value,
                    Contract.start_date <= target_date,
                    Contract.end_date >= target_date,
                )
            )
        )
        contracts = result.scalars().all()
        
        all_bills = []
        for contract in contracts:
            bills = await cls.generate_bills_for_contract(db, contract, target_date)
            all_bills.extend(bills)
        
        await db.commit()
        return all_bills

    @classmethod
    async def update_overdue_bills(cls, db: AsyncSession, check_date: date | None = None) -> int:
        if check_date is None:
            check_date = date.today()
        
        result = await db.execute(
            select(Bill).where(
                and_(
                    Bill.due_date < check_date,
                    Bill.status.in_([BillStatus.UNPAID.value, BillStatus.PARTIAL.value]),
                )
            )
        )
        bills = result.scalars().all()
        
        count = 0
        for bill in bills:
            contract_result = await db.execute(
                select(Contract).where(Contract.id == bill.contract_id)
            )
            contract = contract_result.scalar_one_or_none()
            if not contract:
                continue
            
            monthly_rent = contract.monthly_rent
            late_fee = cls.calculate_late_fee(bill.due_date, check_date, monthly_rent)
            bill.late_fee = late_fee
            bill.total_amount = bill.base_amount + late_fee
            bill.status = BillStatus.OVERDUE.value
            count += 1
        
        await db.commit()
        return count

    @classmethod
    async def record_payment(
        cls,
        db: AsyncSession,
        bill_id: int,
        amount: float,
        payment_method: str = "mock",
        transaction_id: str | None = None,
        note: str = "",
    ) -> Bill:
        result = await db.execute(
            select(Bill).where(Bill.id == bill_id)
        )
        bill = result.scalar_one_or_none()
        if not bill:
            raise ValueError(f"Bill {bill_id} not found")
        
        payment = BillPayment(
            bill_id=bill_id,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            note=note,
        )
        db.add(payment)
        
        bill.paid_amount += amount
        
        if bill.paid_amount >= bill.total_amount:
            bill.status = BillStatus.PAID.value
        elif bill.paid_amount > 0:
            bill.status = BillStatus.PARTIAL.value
        
        await db.commit()
        await db.refresh(bill)
        return bill
