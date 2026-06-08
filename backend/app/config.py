from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Property Management System"
    debug: bool = True
    
    base_dir: Path = Path(__file__).resolve().parent.parent
    database_url: str = f"sqlite+aiosqlite:///{base_dir}/property.db"
    
    late_fee_rate: float = 0.005
    max_late_fee_ratio: float = 0.30
    renewal_reminder_days: int = 30
    early_termination_penalty_rate: float = 0.30
    repair_negotiation_threshold: float = 500.0
    vacancy_gap_days: int = 1

    class Config:
        env_file = ".env"


settings = Settings()
