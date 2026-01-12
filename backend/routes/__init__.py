"""
QR Inventory MVP - API Routes
"""
from .auth_routes import auth_bp
from .site_routes import site_bp

__all__ = ['auth_bp', 'site_bp']
