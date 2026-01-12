"""
Tests for authentication endpoints and middleware
"""
import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ['JWT_SECRET'] = 'test-secret-key-for-testing'
os.environ['ADMIN_PASSWORD'] = 'testpassword123'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import app
from database import Base, engine, SessionLocal
from models.admin import Admin
from services.auth_service import AuthService


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def db_session():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Create test admin user
    password_hash = AuthService.hash_password('testpassword123')
    admin = Admin(username='admin', password_hash=password_hash)
    db.add(admin)
    db.commit()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_login_success(client, db_session):
    """Test successful login"""
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'testpassword123'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['username'] == 'admin'


def test_login_invalid_credentials(client, db_session):
    """Test login with invalid password"""
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data


def test_login_missing_username(client, db_session):
    """Test login with missing username"""
    response = client.post('/api/auth/login', json={
        'password': 'testpassword123'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_login_missing_password(client, db_session):
    """Test login with missing password"""
    response = client.post('/api/auth/login', json={
        'username': 'admin'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_login_short_password(client, db_session):
    """Test login with password less than 8 characters"""
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'short'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_logout(client):
    """Test logout endpoint"""
    response = client.post('/api/auth/logout')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data


def test_protected_route_without_token(client, db_session):
    """Test accessing protected route without token"""
    response = client.get('/api/auth/me')
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data


def test_protected_route_with_invalid_token(client, db_session):
    """Test accessing protected route with invalid token"""
    response = client.get('/api/auth/me', headers={
        'Authorization': 'Bearer invalid-token'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data


def test_protected_route_with_valid_token(client, db_session):
    """Test accessing protected route with valid token"""
    # First login to get token
    login_response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'testpassword123'
    })
    
    token = login_response.get_json()['token']
    
    # Then access protected route
    response = client.get('/api/auth/me', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'admin'


def test_protected_route_invalid_auth_header_format(client, db_session):
    """Test accessing protected route with invalid header format"""
    response = client.get('/api/auth/me', headers={
        'Authorization': 'invalid-format'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
