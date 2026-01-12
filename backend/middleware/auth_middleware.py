"""
Authentication middleware for protected routes
"""
from functools import wraps
from flask import request, jsonify
import jwt
from services.auth_service import AuthService


def require_auth(f):
    """
    Decorator to protect routes requiring authentication.
    Expects Authorization header: Bearer <token>
    Returns consistent error format: {"error": {"code": "...", "message": "..."}}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Authorization header missing'
                }
            }), 401
        
        # Extract token from "Bearer <token>" format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Invalid authorization header format. Expected: Bearer <token>'
                }
            }), 401
        
        token = parts[1]
        
        try:
            payload = AuthService.verify_token(token)
            # Add username to request context for use in route handlers
            request.current_user = payload['username']
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Token has expired'
                }
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Invalid token'
                }
            }), 401
    
    return decorated_function
