"""
Authentication routes - login, logout, me
"""
from flask import Blueprint, request, jsonify
from database import SessionLocal
from services.auth_service import AuthService
from middleware.auth_middleware import require_auth

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint
    POST /api/auth/login
    Body: {"username": "admin", "password": "secret"}
    Returns: {"token": "<jwt>", "username": "admin"}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Validate password length
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    db = SessionLocal()
    try:
        admin = AuthService.authenticate(db, username, password)
        
        if not admin:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        token = AuthService.generate_token(admin.username)
        
        return jsonify({
            'token': token,
            'username': admin.username
        }), 200
    finally:
        db.close()


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout endpoint (stateless - client deletes token)
    POST /api/auth/logout
    Returns: {"message": "Logged out successfully"}
    """
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """
    Get current authenticated user
    GET /api/auth/me
    Headers: Authorization: Bearer <token>
    Returns: {"username": "admin"}
    """
    return jsonify({
        'username': request.current_user
    }), 200
