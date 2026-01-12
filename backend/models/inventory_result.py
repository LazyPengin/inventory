"""
InventoryResult model - Represents the status of a single item in an inventory check
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


class InventoryStatus(enum.Enum):
    """Enum for inventory item status"""
    PRESENT = 'present'
    MISSING = 'missing'
    NOT_ENOUGH = 'not_enough'
    BATTERY_LOW = 'battery_low'


class InventoryResult(Base):
    """InventoryResult model - Status of a single item in inventory check"""
    __tablename__ = 'inventory_results'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('inventory_sessions.id', ondelete='CASCADE'), nullable=False)
    # bag_item_id nullable: allows reporting items not in expected checklist (future flexibility)
    bag_item_id = Column(Integer, ForeignKey('bag_items.id', ondelete='SET NULL'), nullable=True)
    # Status enum: present, missing, not_enough, battery_low
    status = Column(Enum(InventoryStatus), nullable=False)
    # observed_qty: actual quantity counted (relevant for "not_enough" status)
    observed_qty = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    session = relationship('InventorySession', back_populates='inventory_results')
    bag_item = relationship('BagItem', back_populates='inventory_results')

    def __repr__(self):
        return f"<InventoryResult(id={self.id}, session_id={self.session_id}, status={self.status.value})>"
