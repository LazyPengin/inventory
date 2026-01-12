"""
Site model - Represents a physical location with bags/kits
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Site(Base):
    """Site model - Physical location containing multiple bags"""
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    # JSON array of email addresses stored as TEXT (SQLite-friendly)
    # Example: '["admin@example.com", "safety@example.com"]'
    alert_recipients = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # Note: No cascade delete - bags must be deleted manually (RESTRICT behavior)
    bags = relationship('Bag', back_populates='site')

    def __repr__(self):
        return f"<Site(id={self.id}, name={self.name})>"
