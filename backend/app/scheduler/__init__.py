import asyncio
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..database import async_session
from ..services import BillService

scheduler = AsyncIOScheduler()


async def generate_monthly_bills_job():
    async with async_session() as db:
        bills = await BillService.generate_monthly_bills(db)
        print(f"[Scheduler] Generated {len(bills)} bills at {date.today()}")


async def check_overdue_bills_job():
    async with async_session() as db:
        count = await BillService.update_overdue_bills(db)
        print(f"[Scheduler] Found {count} overdue bills at {date.today()}")


def start_scheduler():
    scheduler.add_job(
        generate_monthly_bills_job,
        trigger=CronTrigger(day=1, hour=3, minute=0),
        id="monthly_bill_generation",
        replace_existing=True,
    )
    
    scheduler.add_job(
        check_overdue_bills_job,
        trigger=CronTrigger(hour=3, minute=30),
        id="daily_overdue_check",
        replace_existing=True,
    )
    
    scheduler.start()
    print("[Scheduler] Scheduler started")


def stop_scheduler():
    scheduler.shutdown()
    print("[Scheduler] Scheduler stopped")


__all__ = ["scheduler", "start_scheduler", "stop_scheduler"]
