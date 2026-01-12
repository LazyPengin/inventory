"""
Bag model - Represents a physical bag/kit at a site
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Bag(Base):
    """Bag model - Physical bag/kit with QR code"""
    __tablename__ = 'bags'

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sites.id', ondelete='RESTRICT'), nullable=False)
    name = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    # QR token - unique identifier for bag (UUIDv4 format)
    qr_token = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    site = relationship('Site', back_populates='bags')
    bag_items = relationship('BagItem', back_populates='bag', cascade='all, delete-orphan')
    inventory_sessions = relationship('InventorySession', back_populates='bag')

    def __repr__(self):
        return f"<Bag(id={self.id}, name={self.name}, qr_token={self.qr_token})>"
