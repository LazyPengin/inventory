"""
Seed script to create default admin user
Run with: python seed_admin.py
"""
import os
import sys
from dotenv import load_dotenv
from database import SessionLocal
from models.admin import Admin
from services.auth_service import AuthService

load_dotenv()


def seed_admin():
    """Create default admin user from environment variables"""
    
    # Get credentials from environment
    username = os.getenv('ADMIN_USERNAME', 'admin')
    password = os.getenv('ADMIN_PASSWORD')
    
    if not password:
        print("ERROR: ADMIN_PASSWORD environment variable is required")
        print("Set it in your .env file: ADMIN_PASSWORD=your_secure_password")
        sys.exit(1)
    
    if len(password) < 8:
        print("ERROR: ADMIN_PASSWORD must be at least 8 characters")
        sys.exit(1)
    
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(Admin).filter(Admin.username == username).first()
        
        if existing_admin:
            print(f"Admin user '{username}' already exists")
            return
        
        # Create admin user
        password_hash = AuthService.hash_password(password)
        admin = Admin(username=username, password_hash=password_hash)
        
        db.add(admin)
        db.commit()
        
        print(f"✓ Admin user '{username}' created successfully")
        print(f"  Username: {username}")
        print(f"  Password: (set from ADMIN_PASSWORD env var)")
    except Exception as e:
        db.rollback()
        print(f"✗ Failed to create admin user: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == '__main__':
    seed_admin()
