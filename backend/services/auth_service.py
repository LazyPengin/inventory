"""
Authentication service - handles login, token generation, password hashing
"""
import os
import jwt
import bcrypt as bcrypt_lib
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from models.admin import Admin


class AuthService:
    """Handles authentication logic"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt_lib.gensalt()
        hashed = bcrypt_lib.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt_lib.checkpw(password_bytes, hashed_bytes)

    @staticmethod
    def generate_token(username: str) -> str:
        """Generate JWT token for authenticated user"""
        secret = os.getenv('JWT_SECRET')
        expires_hours = int(os.getenv('JWT_EXPIRES_HOURS', '8'))

        now = datetime.now(timezone.utc)
        payload = {
            'username': username,
            'exp': now + timedelta(hours=expires_hours),
            'iat': now
        }
        
        return jwt.encode(payload, secret, algorithm='HS256')

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify JWT token and return payload.
        Raises jwt.ExpiredSignatureError if expired.
        Raises jwt.InvalidTokenError if invalid.
        """
        secret = os.getenv('JWT_SECRET')
        return jwt.decode(token, secret, algorithms=['HS256'])

    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> Admin:
        """
        Authenticate user with username and password.
        Returns Admin object if successful, None otherwise.
        """
        admin = db.query(Admin).filter(Admin.username == username).first()
        
        if not admin:
            return None
        
        if not AuthService.verify_password(password, admin.password_hash):
            return None
        
        return admin
