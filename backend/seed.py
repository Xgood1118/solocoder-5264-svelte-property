import asyncio
import sys
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

sys.path.insert(0, '.')

from app.database import async_session, init_db
from app.models import Property, Tenant, Contract, Bill, Repair, ContractStatus, BillStatus, RepairStatus, RepairUrgency
from app.services.bill_service import BillService


async def seed_data():
    await init_db()
    
    async with async_session() as db:
        properties = [
            Property(
                address="朝阳区阳光花园1号楼3单元501室",
                house_type="两室一厅",
                area=85.5,
                floor="5/6层",
                decoration_status="精装",
                is_rented=True,
                note="南北通透，采光好",
            ),
            Property(
                address="海淀区中关村南大街12号院2号楼102室",
                house_type="一室一厅",
                area=55.0,
                floor="1/18层",
                decoration_status="简装",
                is_rented=True,
                note="学区房",
            ),
            Property(
                address="西城区金融街甲3号4号楼1503室",
                house_type="三室两厅",
                area=120.0,
                floor="15/28层",
                decoration_status="豪装",
                is_rented=False,
                note="高端小区，物业管理好",
            ),
            Property(
                address="丰台区方庄芳城园3区7号楼402室",
                house_type="两室一厅",
                area=78.0,
                floor="4/6层",
                decoration_status="简装",
                is_rented=True,
                note="交通便利，近地铁",
            ),
            Property(
                address="昌平区回龙观龙泽苑西区5号楼3单元601室",
                house_type="两室一厅",
                area=90.0,
                floor="6/6层",
                decoration_status="中装",
                is_rented=False,
                note="顶层带阁楼",
            ),
        ]
        db.add_all(properties)
        await db.flush()
        
        tenants = [
            Tenant(
                name="张三",
                phone="13800138001",
                id_card="110101199001011234",
                emergency_contact="张母",
                emergency_phone="13900139001",
                address="河北省石家庄市",
            ),
            Tenant(
                name="李四",
                phone="13800138002",
                id_card="110102199202022345",
                emergency_contact="李父",
                emergency_phone="13900139002",
            ),
            Tenant(
                name="王五",
                phone="13800138003",
                id_card="110103198803033456",
                emergency_contact="王妻",
                emergency_phone="13900139003",
            ),
        ]
        db.add_all(tenants)
        await db.flush()
        
        today = date.today()
        contracts = [
            Contract(
                property_id=properties[0].id,
                tenant_id=tenants[0].id,
                start_date=today - relativedelta(months=6),
                end_date=today + relativedelta(months=6),
                monthly_rent=3500.0,
                deposit=7000.0,
                payment_cycle="monthly",
                rent_due_day=1,
                status=ContractStatus.ACTIVE.value,
                note="房东直租，一年起租",
            ),
            Contract(
                property_id=properties[1].id,
                tenant_id=tenants[1].id,
                start_date=today - relativedelta(months=3),
                end_date=today + relativedelta(months=9),
                monthly_rent=2800.0,
                deposit=5600.0,
                payment_cycle="quarterly",
                rent_due_day=5,
                status=ContractStatus.ACTIVE.value,
            ),
            Contract(
                property_id=properties[3].id,
                tenant_id=tenants[2].id,
                start_date=today - relativedelta(months=11),
                end_date=today + relativedelta(days=20),
                monthly_rent=3200.0,
                deposit=6400.0,
                payment_cycle="monthly",
                rent_due_day=1,
                status=ContractStatus.ACTIVE.value,
                note="即将到期，待续约",
            ),
        ]
        db.add_all(contracts)
        await db.flush()
        
        for contract in contracts:
            for i in range(6):
                ref_date = contract.start_date + relativedelta(months=i)
                if ref_date > today:
                    break
                await BillService.generate_bills_for_contract(db, contract, ref_date)
        
        repairs = [
            Repair(
                property_id=properties[0].id,
                tenant_id=tenants[0].id,
                contract_id=contracts[0].id,
                title="卫生间水龙头漏水",
                description="卫生间洗手池水龙头关不紧，一直滴水",
                urgency=RepairUrgency.LOW.value,
                status=RepairStatus.SUBMITTED.value,
            ),
            Repair(
                property_id=properties[1].id,
                tenant_id=tenants[1].id,
                contract_id=contracts[1].id,
                title="空调不制冷",
                description="夏天到了，空调开了没冷风，可能需要加氟",
                urgency=RepairUrgency.HIGH.value,
                status=RepairStatus.IN_PROGRESS.value,
                assigned_to="王师傅",
                cost_estimate=200.0,
            ),
            Repair(
                property_id=properties[3].id,
                tenant_id=tenants[2].id,
                contract_id=contracts[2].id,
                title="厨房下水道堵塞",
                description="厨房水槽下水很慢，可能是油污堵塞",
                urgency=RepairUrgency.MEDIUM.value,
                status=RepairStatus.COMPLETED.value,
                assigned_to="李师傅",
                actual_cost=150.0,
                cost_responsibility="landlord",
            ),
        ]
        db.add_all(repairs)
        await db.flush()
        
        await db.commit()
        
        print(f"✅ 种子数据创建成功！")
        print(f"   房源：{len(properties)} 套")
        print(f"   租客：{len(tenants)} 人")
        print(f"   合同：{len(contracts)} 份")
        print(f"   维修工单：{len(repairs)} 张")


if __name__ == "__main__":
    asyncio.run(seed_data())
