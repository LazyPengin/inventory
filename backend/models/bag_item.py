"""
BagItem model - Represents an expected item in a bag
Note: Table name is 'bag_items' (approved deviation from tasks.md which used 'items')
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class BagItem(Base):
    """BagItem model - Expected item in a bag with tracking configuration"""
    __tablename__ = 'bag_items'

    id = Column(Integer, primary_key=True, index=True)
    bag_id = Column(Integer, ForeignKey('bags.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    # expected_qty nullable: NULL means "presence-only check" (yes/no)
    expected_qty = Column(Integer, nullable=True)
    track_expiry = Column(Boolean, nullable=False, default=False)
    # expiry_date only relevant if track_expiry=True
    expiry_date = Column(Date, nullable=True)
    # test_batteries corresponds to "requires_battery_test" in tasks.md
    test_batteries = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    bag = relationship('Bag', back_populates='bag_items')
    inventory_results = relationship('InventoryResult', back_populates='bag_item')

    def __repr__(self):
        return f"<BagItem(id={self.id}, name={self.name}, bag_id={self.bag_id})>"
