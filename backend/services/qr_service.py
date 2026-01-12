"""
QR service - Business logic for QR token lookup
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from models.bag import Bag
from models.bag_item import BagItem
from services.bag_item_service import BagItemService


class QRService:
    """Handles QR token lookup logic"""

    @staticmethod
    def lookup_by_qr_token(db: Session, qr_token: str) -> Optional[Dict[str, Any]]:
        """
        Look up a bag by its QR token and return bag + items.
        
        Args:
            db: Database session
            qr_token: The QR token to look up
        
        Returns:
            dict with 'bag' and 'items' keys, or None if not found or inactive
        
        Raises:
            ValueError: if qr_token is invalid/not found or bag is inactive
        """
        # Look up bag by qr_token
        bag = db.query(Bag).filter(Bag.qr_token == qr_token).first()
        
        if not bag:
            raise ValueError("Bag not found")
        
        # Check if bag is active
        if not bag.active:
            raise ValueError("Bag not found")
        
        # Get items for this bag (ordered by created_at)
        items = db.query(BagItem).filter(
            BagItem.bag_id == bag.id
        ).order_by(BagItem.created_at).all()
        
        # Convert to response format
        return {
            'bag': {
                'id': bag.id,
                'site_id': bag.site_id,
                'name': bag.name,
                'active': bag.active
            },
            'items': [BagItemService.bag_item_to_dict(item) for item in items]
        }
