"""
BagItem service - business logic for bag item management
"""
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from models.bag_item import BagItem
from models.bag import Bag


class BagItemService:
    """Handles bag item business logic and validation"""

    @staticmethod
    def validate_bag_item_data(data: dict, is_update: bool = False) -> tuple[bool, str | None]:
        """
        Validate bag item data.
        
        Args:
            data: dict of item fields
            is_update: if True, all fields are optional
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Name validation
        if not is_update:
            if 'name' not in data or not data.get('name'):
                return False, "name is required"
        else:
            if 'name' in data and not data['name']:
                return False, "name cannot be empty"
        
        # Expected quantity validation
        if 'expected_qty' in data and data['expected_qty'] is not None:
            try:
                qty = int(data['expected_qty'])
                if qty < 0:
                    return False, "expected_qty must be >= 0"
            except (ValueError, TypeError):
                return False, "expected_qty must be an integer"
        
        # Expiry date validation
        if 'expiry_date' in data and data['expiry_date'] is not None:
            # Check if track_expiry is true
            track_expiry = data.get('track_expiry', False)
            if not track_expiry:
                return False, "expiry_date requires track_expiry to be true"
            
            # Validate date format (YYYY-MM-DD) and parse to date object
            from datetime import datetime, date
            if isinstance(data['expiry_date'], str):
                try:
                    # Parse and convert string to date object
                    parsed_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
                    # Replace string with date object in data
                    data['expiry_date'] = parsed_date
                except ValueError:
                    return False, "expiry_date must be in YYYY-MM-DD format"
            elif not isinstance(data['expiry_date'], date):
                return False, "expiry_date must be a date string (YYYY-MM-DD) or date object"
        
        # Immutable field check for updates
        if is_update and 'bag_id' in data:
            return False, "bag_id is immutable and cannot be changed"
        
        return True, None


    @staticmethod
    def create_bag_item(db: Session, bag_id: int, data: Dict[str, Any]) -> BagItem:
        """
        Create a new bag item.
        
        Args:
            db: Database session
            bag_id: ID of the parent bag
            data: dict with item fields
        
        Returns:
            BagItem: created item
        
        Raises:
            ValueError: if validation fails or bag doesn't exist
        """
        # Validate bag exists
        bag = db.query(Bag).filter(Bag.id == bag_id).first()
        if not bag:
            raise KeyError("Bag not found")
        
        # Validate data
        is_valid, error_msg = BagItemService.validate_bag_item_data(data, is_update=False)
        if not is_valid:
            raise ValueError(error_msg)
        
        # Create item
        item = BagItem(
            bag_id=bag_id,
            name=data['name'].strip(),
            expected_qty=data.get('expected_qty'),
            track_expiry=data.get('track_expiry', False),
            expiry_date=data.get('expiry_date'),
            test_batteries=data.get('test_batteries', False)
        )
        
        db.add(item)
        db.commit()
        db.refresh(item)
        
        return item
    
    @staticmethod
    def get_bag_items(db: Session, bag_id: int) -> List[Any]:
        """
        Get all items for a bag.
        
        Args:
            db: Database session
            bag_id: ID of the bag
        
        Returns:
            list[BagItem]: list of items
        
        Raises:
            ValueError: if bag doesn't exist
        """
        from models.bag import Bag
        
        # Validate bag exists
        bag = db.query(Bag).filter(Bag.id == bag_id).first()
        if not bag:
            raise ValueError("Bag not found")
        
        items = db.query(BagItem).filter(BagItem.bag_id == bag_id).order_by(BagItem.created_at).all()
        return items
    
    @staticmethod
    def get_bag_item_by_id(db: Session, item_id: int):
        """
        Get a bag item by ID.
        
        Args:
            db: Database session
            item_id: ID of the item
        
        Returns:
            BagItem: the item
        
        Raises:
            KeyError: if item doesn't exist
        """
        item = db.query(BagItem).filter(BagItem.id == item_id).first()
        if not item:
            raise KeyError(f"Item not found")
        return item
    
    @staticmethod
    def update_bag_item(db: Session, item_id: int, data: Dict[str, Any]):
        """
        Update a bag item (partial update).
        
        Args:
            db: database session
            item_id: ID of the item to update
            data: dict with fields to update
        
        Returns:
            updated BagItem
        
        Raises:
            KeyError: if item doesn't exist
            ValueError: if validation fails or no fields provided
        """
        # Get existing item
        item = db.query(BagItem).filter(BagItem.id == item_id).first()
        if not item:
            raise KeyError(f"Item not found")
        
        # Validate data
        is_valid, error_msg = BagItemService.validate_bag_item_data(data, is_update=True)
        if not is_valid:
            raise ValueError(error_msg)
        
        # Check at least one field is provided
        allowed_fields = {'name', 'expected_qty', 'track_expiry', 'expiry_date', 'test_batteries'}
        provided_fields = set(data.keys()) & allowed_fields
        if not provided_fields:
            raise ValueError("at least one field (name, expected_qty, track_expiry, expiry_date, test_batteries) must be provided")
        
        # Update fields
        if 'name' in data:
            item.name = data['name'].strip()
        if 'expected_qty' in data:
            item.expected_qty = data['expected_qty']
        if 'track_expiry' in data:
            item.track_expiry = data['track_expiry']
        if 'expiry_date' in data:
            item.expiry_date = data['expiry_date']
        if 'test_batteries' in data:
            item.test_batteries = data['test_batteries']
        
        # SQLAlchemy will handle updated_at automatically via onupdate
        db.commit()
        db.refresh(item)
        
        return item
    
    @staticmethod
    def delete_bag_item(db: Session, item_id: int):
        """
        Delete a bag item.
        
        Per DB-1 schema: inventory_results.bag_item_id has ON DELETE SET NULL,
        so delete will always succeed even if results exist.
        
        Args:
            db: database session
            item_id: ID of the item to delete
        
        Raises:
            KeyError: if item doesn't exist
        """
        item = db.query(BagItem).filter(BagItem.id == item_id).first()
        if not item:
            raise KeyError(f"Item not found")
        
        db.delete(item)
        db.commit()
    
    @staticmethod
    def bag_item_to_dict(item):
        """
        Convert BagItem to dict.
        
        Args:
            item: BagItem instance
        
        Returns:
            dict: item data
        """
        from datetime import date
        return {
            'id': item.id,
            'bag_id': item.bag_id,
            'name': item.name,
            'expected_qty': item.expected_qty,
            'track_expiry': item.track_expiry,
            'expiry_date': item.expiry_date.isoformat() if isinstance(item.expiry_date, date) else item.expiry_date,
            'test_batteries': item.test_batteries,
            'created_at': item.created_at.isoformat() if item.created_at else None,
            'updated_at': item.updated_at.isoformat() if item.updated_at else None
        }
