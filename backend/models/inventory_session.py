"""
InventorySession model - Represents a single inventory check event
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class InventorySession(Base):
    """InventorySession model - A single inventory check event"""
    __tablename__ = 'inventory_sessions'

    id = Column(Integer, primary_key=True, index=True)
    bag_id = Column(Integer, ForeignKey('bags.id', ondelete='RESTRICT'), nullable=False)
    # created_at indexed for metrics queries (completion rate, duration)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    # Optional user identification
    nickname = Column(String(255), nullable=True)
    # Geolocation data (all nullable - geolocation can fail)
    ip_address = Column(String(45), nullable=True)  # IPv6-compatible (45 chars)
    geo_city = Column(String(255), nullable=True)
    geo_country = Column(String(255), nullable=True)

    # Relationships
    bag = relationship('Bag', back_populates='inventory_sessions')
    inventory_results = relationship('InventoryResult', back_populates='session', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<InventorySession(id={self.id}, bag_id={self.bag_id}, created_at={self.created_at})>"
