from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ..models import Contract, RenewalRequest, RenewalStatus, ContractStatus
from ..config import settings


class RenewalService:
    @staticmethod
    def is_renewal_available(contract: Contract, check_date: date | None = None) -> bool:
        if check_date is None:
            check_date = date.today()
        
        if contract.status != ContractStatus.ACTIVE.value:
            return False
        
        days_until_expiry = (contract.end_date - check_date).days
        return days_until_expiry <= settings.renewal_reminder_days

    @staticmethod
    def validate_vacancy_gap(
        old_end_date: date,
        new_start_date: date,
        gap_days: int | None = None,
    ) -> tuple[bool, str]:
        if gap_days is None:
            gap_days = settings.vacancy_gap_days
        
        actual_gap = (new_start_date - old_end_date).days
        
        if actual_gap < gap_days:
            return False, f"新旧合同之间需要至少{gap_days}天空房期（清洁时间），当前间隔{actual_gap}天"
        
        return True, "校验通过"

    @classmethod
    async def create_renewal_request(
        cls,
        db: AsyncSession,
        contract_id: int,
        new_start_date: date,
        new_end_date: date,
        new_monthly_rent: float,
        new_deposit: float = 0.0,
        new_payment_cycle: str | None = None,
        tenant_note: str = "",
    ) -> RenewalRequest:
        result = await db.execute(
            select(Contract).where(Contract.id == contract_id)
        )
        contract = result.scalar_one_or_none()
        if not contract:
            raise ValueError(f"Contract {contract_id} not found")
        
        valid, msg = cls.validate_vacancy_gap(contract.end_date, new_start_date)
        if not valid:
            raise ValueError(msg)
        
        if new_end_date <= new_start_date:
            raise ValueError("新合同结束日期必须晚于开始日期")
        
        existing_pending = await db.execute(
            select(RenewalRequest).where(
                and_(
                    RenewalRequest.contract_id == contract_id,
                    RenewalRequest.status == RenewalStatus.PENDING.value,
                )
            )
        )
        if existing_pending.scalar_one_or_none():
            raise ValueError("已有待审核的续约申请")
        
        request = RenewalRequest(
            contract_id=contract_id,
            new_start_date=new_start_date,
            new_end_date=new_end_date,
            new_monthly_rent=new_monthly_rent,
            new_deposit=new_deposit if new_deposit is not None else contract.deposit,
            new_payment_cycle=new_payment_cycle or contract.payment_cycle,
            tenant_note=tenant_note,
            status=RenewalStatus.PENDING.value,
        )
        
        db.add(request)
        await db.commit()
        await db.refresh(request)
        return request

    @classmethod
    async def approve_renewal(
        cls,
        db: AsyncSession,
        request_id: int,
        landlord_note: str = "",
    ) -> tuple[RenewalRequest, Contract]:
        result = await db.execute(
            select(RenewalRequest).where(RenewalRequest.id == request_id)
        )
        request = result.scalar_one_or_none()
        if not request:
            raise ValueError(f"Renewal request {request_id} not found")
        
        if request.status != RenewalStatus.PENDING.value:
            raise ValueError("只有待审核的申请可以审批")
        
        contract_result = await db.execute(
            select(Contract).where(Contract.id == request.contract_id)
        )
        old_contract = contract_result.scalar_one_or_none()
        if not old_contract:
            raise ValueError("关联合同不存在")
        
        from datetime import datetime
        new_contract = Contract(
            property_id=old_contract.property_id,
            tenant_id=old_contract.tenant_id,
            start_date=request.new_start_date,
            end_date=request.new_end_date,
            monthly_rent=request.new_monthly_rent,
            deposit=request.new_deposit,
            payment_cycle=request.new_payment_cycle or old_contract.payment_cycle,
            rent_due_day=old_contract.rent_due_day,
            renewal_option=old_contract.renewal_option,
            status=ContractStatus.ACTIVE.value,
            note=f"续约自合同 #{old_contract.id}",
        )
        
        old_contract.status = ContractStatus.EXPIRED.value
        
        request.status = RenewalStatus.APPROVED.value
        request.landlord_note = landlord_note
        request.reviewed_at = datetime.utcnow()
        
        db.add(new_contract)
        await db.commit()
        await db.refresh(request)
        await db.refresh(new_contract)
        
        return request, new_contract

    @classmethod
    async def reject_renewal(
        cls,
        db: AsyncSession,
        request_id: int,
        landlord_note: str = "",
    ) -> RenewalRequest:
        result = await db.execute(
            select(RenewalRequest).where(RenewalRequest.id == request_id)
        )
        request = result.scalar_one_or_none()
        if not request:
            raise ValueError(f"Renewal request {request_id} not found")
        
        if request.status != RenewalStatus.PENDING.value:
            raise ValueError("只有待审核的申请可以审批")
        
        from datetime import datetime
        request.status = RenewalStatus.REJECTED.value
        request.landlord_note = landlord_note
        request.reviewed_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(request)
        return request
