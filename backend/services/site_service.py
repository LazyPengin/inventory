"""
Site service - Business logic for site management
"""
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.site import Site


class SiteService:
    """Handles site business logic and validation"""

    @staticmethod
    def validate_alert_recipients(recipients: Any) -> List[str]:
        """
        MVP-simple validation for alert recipients.
        
        Rules:
        - Must be a list
        - Each entry must be a non-empty string
        - Each entry must contain '@' and '.'
        """
        if not isinstance(recipients, list):
            raise ValueError("alert_recipients must be a list")
        
        if len(recipients) == 0:
            raise ValueError("alert_recipients must contain at least one email")
        
        for email in recipients:
            if not isinstance(email, str) or not email.strip():
                raise ValueError("alert_recipients entries must be non-empty strings")
            if '@' not in email or '.' not in email:
                raise ValueError("alert_recipients entries must contain '@' and '.'")
        
        return recipients

    @staticmethod
    def serialize_alert_recipients(recipients: List[str]) -> str:
        """Convert list to JSON string for database storage"""
        return json.dumps(recipients)

    @staticmethod
    def deserialize_alert_recipients(recipients_json: str) -> List[str]:
        """Convert JSON string from database to list"""
        return json.loads(recipients_json)

    @staticmethod
    def create_site(db: Session, name: str, alert_recipients: List[str]) -> Site:
        """Create a new site"""
        # Validate inputs
        if not name or not name.strip():
            raise ValueError("name is required and must not be empty")
        
        validated_recipients = SiteService.validate_alert_recipients(alert_recipients)
        recipients_json = SiteService.serialize_alert_recipients(validated_recipients)
        
        # Create site
        site = Site(
            name=name.strip(),
            alert_recipients=recipients_json
        )
        
        db.add(site)
        db.commit()
        db.refresh(site)
        
        return site

    @staticmethod
    def get_all_sites(db: Session) -> List[Site]:
        """Get all sites"""
        return db.query(Site).order_by(Site.created_at.desc()).all()

    @staticmethod
    def get_site_by_id(db: Session, site_id: int) -> Site:
        """Get site by ID, raises ValueError if not found"""
        site = db.query(Site).filter(Site.id == site_id).first()
        if not site:
            raise ValueError("Site not found")
        return site

    @staticmethod
    def update_site(db: Session, site_id: int, name: str = None, alert_recipients: List[str] = None) -> Site:
        """Update site (partial update)"""
        site = SiteService.get_site_by_id(db, site_id)
        
        # Update name if provided
        if name is not None:
            if not name.strip():
                raise ValueError("name must not be empty if provided")
            site.name = name.strip()
        
        # Update alert_recipients if provided
        if alert_recipients is not None:
            validated_recipients = SiteService.validate_alert_recipients(alert_recipients)
            site.alert_recipients = SiteService.serialize_alert_recipients(validated_recipients)
        
        db.commit()
        db.refresh(site)
        
        return site

    @staticmethod
    def delete_site(db: Session, site_id: int) -> None:
        """Delete site, raises ValueError if has bags (FK constraint)"""
        site = SiteService.get_site_by_id(db, site_id)
        
        db.delete(site)
        db.commit()

    @staticmethod
    def site_to_dict(site: Site) -> Dict[str, Any]:
        """Convert Site model to dictionary for API response"""
        return {
            "id": site.id,
            "name": site.name,
            "alert_recipients": SiteService.deserialize_alert_recipients(site.alert_recipients),
            "created_at": site.created_at.isoformat() if site.created_at else None,
            "updated_at": site.updated_at.isoformat() if site.updated_at else None
        }
