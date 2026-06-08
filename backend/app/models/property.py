from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(500), nullable=False, index=True)
    house_type = Column(String(50))
    area = Column(Float)
    floor = Column(String(50))
    decoration_status = Column(String(50))
    photo_urls = Column(Text, default="")
    is_rented = Column(Boolean, default=False)
    note = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    contracts = relationship("Contract", back_populates="property")
    repairs = relationship("Repair", back_populates="property")
