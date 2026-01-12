"""
Bag service - Business logic for bag management and qr_token generation
"""
import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.bag import Bag
from models.site import Site


class BagService:
    """Handles bag business logic and qr_token generation"""

    @staticmethod
    def generate_qr_token(db: Session) -> str:
        """
        Generate unique qr_token for bag using UUID4.
        Retries on collision (extremely unlikely).
        
        Returns:
            str: Unique qr_token in UUID4 format
        
        Raises:
            RuntimeError: If unable to generate unique token after retries
        """
        max_retries = 5
        for attempt in range(max_retries):
            token = str(uuid.uuid4())
            
            # Check uniqueness
            existing = db.query(Bag).filter(Bag.qr_token == token).first()
            if not existing:
                return token
        
        # Should never happen with UUID4 (collision probability ~1 in 10^36)
        raise RuntimeError("Failed to generate unique qr_token after retries")

    @staticmethod
    def create_bag(db: Session, site_id: int, name: str) -> Bag:
        """
        Create a new bag with server-generated qr_token.
        
        Args:
            db: Database session
            site_id: ID of the site this bag belongs to
            name: Name of the bag
        
        Returns:
            Bag: Created bag object
        
        Raises:
            ValueError: If validation fails or site not found
        """
        # Validate inputs
        if not name or not name.strip():
            raise ValueError("name is required and must not be empty")
        
        # Verify site exists
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            raise ValueError("Site not found")
        
        # Generate unique qr_token
        qr_token = BagService.generate_qr_token(db)
        
        # Create bag
        bag = Bag(
            site_id=site_id,
            name=name.strip(),
            qr_token=qr_token,
            active=True  # Default
        )
        
        db.add(bag)
        db.commit()
        db.refresh(bag)
        
        return bag

    @staticmethod
    def get_bags_by_site(db: Session, site_id: int) -> List[Bag]:
        """
        Get all bags for a specific site.
        
        Args:
            db: Database session
            site_id: ID of the site
        
        Returns:
            List[Bag]: List of bags for the site
        
        Raises:
            ValueError: If site not found
        """
        # Verify site exists
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            raise ValueError("Site not found")
        
        return db.query(Bag).filter(Bag.site_id == site_id).order_by(Bag.created_at.desc()).all()

    @staticmethod
    def get_bag_by_id(db: Session, bag_id: int) -> Bag:
        """
        Get bag by ID.
        
        Args:
            db: Database session
            bag_id: ID of the bag
        
        Returns:
            Bag: Bag object
        
        Raises:
            ValueError: If bag not found
        """
        bag = db.query(Bag).filter(Bag.id == bag_id).first()
        if not bag:
            raise ValueError("Bag not found")
        return bag

    @staticmethod
    def update_bag(db: Session, bag_id: int, name: str = None, active: bool = None) -> Bag:
        """
        Update bag (partial update).
        qr_token and site_id are immutable.
        
        Args:
            db: Database session
            bag_id: ID of the bag
            name: New name (optional)
            active: New active status (optional)
        
        Returns:
            Bag: Updated bag object
        
        Raises:
            ValueError: If bag not found or validation fails
        """
        bag = BagService.get_bag_by_id(db, bag_id)
        
        # Update name if provided
        if name is not None:
            if not name.strip():
                raise ValueError("name must not be empty if provided")
            bag.name = name.strip()
        
        # Update active if provided
        if active is not None:
            if not isinstance(active, bool):
                raise ValueError("active must be a boolean")
            bag.active = active
        
        db.commit()
        db.refresh(bag)
        
        return bag

    @staticmethod
    def delete_bag(db: Session, bag_id: int) -> None:
        """
        Delete bag.
        Cascade deletes bag_items (per DB-1 schema).
        Raises error if bag has inventory_sessions (FK RESTRICT).
        
        Args:
            db: Database session
            bag_id: ID of the bag
        
        Raises:
            ValueError: If bag not found
            IntegrityError: If bag has inventory sessions (FK RESTRICT)
        """
        bag = BagService.get_bag_by_id(db, bag_id)
        
        db.delete(bag)
        db.commit()

    @staticmethod
    def bag_to_dict(bag: Bag) -> Dict[str, Any]:
        """
        Convert Bag model to dictionary for API response.
        
        Args:
            bag: Bag model instance
        
        Returns:
            Dict: Bag data as dictionary
        """
        return {
            "id": bag.id,
            "site_id": bag.site_id,
            "name": bag.name,
            "qr_token": bag.qr_token,
            "active": bag.active,
            "created_at": bag.created_at.isoformat() if bag.created_at else None,
            "updated_at": bag.updated_at.isoformat() if bag.updated_at else None
        }
