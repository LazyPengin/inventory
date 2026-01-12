"""
Tests for Bag CRUD endpoints (BE-3)
All endpoints require JWT authentication
"""
import pytest
import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ['JWT_SECRET'] = 'test-secret-key-for-testing'
os.environ['ADMIN_PASSWORD'] = 'testpassword123'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['TESTING'] = 'true'

from app import app
from database import Base, engine, SessionLocal
from models import Admin, Site, Bag, InventorySession
from services.auth_service import AuthService


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def db_session():
    """Create test database session with admin user"""
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


@pytest.fixture
def auth_token(client, db_session):
    """Get valid JWT token for authentication"""
    response = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'testpassword123'
    })
    return response.get_json()['token']


@pytest.fixture
def test_site(db_session):
    """Create a test site"""
    alert_emails = json.dumps(['admin@example.com'])
    site = Site(name='Test Site', alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    return site


# Authentication tests (5 tests)

def test_create_bag_without_auth(client, db_session, test_site):
    """Test POST /api/sites/<site_id>/bags without auth returns 401"""
    response = client.post(f'/api/sites/{test_site.id}/bags', json={
        'name': 'Test Bag'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_list_bags_without_auth(client, db_session, test_site):
    """Test GET /api/sites/<site_id>/bags without auth returns 401"""
    response = client.get(f'/api/sites/{test_site.id}/bags')
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_get_bag_without_auth(client, db_session):
    """Test GET /api/bags/<id> without auth returns 401"""
    response = client.get('/api/bags/1')
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_update_bag_without_auth(client, db_session):
    """Test PATCH /api/bags/<id> without auth returns 401"""
    response = client.patch('/api/bags/1', json={
        'name': 'Updated Bag'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_delete_bag_without_auth(client, db_session):
    """Test DELETE /api/bags/<id> without auth returns 401"""
    response = client.delete('/api/bags/1')
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


# Create tests (4 tests)

def test_create_bag_success(client, db_session, auth_token, test_site):
    """Test POST /api/sites/<site_id>/bags with valid data returns 201 with qr_token"""
    response = client.post(f'/api/sites/{test_site.id}/bags',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'First Aid Kit'}
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] is not None
    assert data['site_id'] == test_site.id
    assert data['name'] == 'First Aid Kit'
    assert data['qr_token'] is not None
    assert len(data['qr_token']) == 36  # UUID4 format with hyphens
    assert data['active'] is True
    assert data['created_at'] is not None
    assert data['updated_at'] is None


def test_create_bag_generates_unique_tokens(client, db_session, auth_token, test_site):
    """Test POST creates unique qr_token for each bag"""
    # Create first bag
    response1 = client.post(f'/api/sites/{test_site.id}/bags',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'Bag 1'}
    )
    token1 = response1.get_json()['qr_token']
    
    # Create second bag
    response2 = client.post(f'/api/sites/{test_site.id}/bags',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'Bag 2'}
    )
    token2 = response2.get_json()['qr_token']
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    assert token1 != token2  # Tokens must be different


def test_create_bag_invalid_site(client, db_session, auth_token):
    """Test POST /api/sites/<site_id>/bags with invalid site_id returns 404"""
    response = client.post('/api/sites/9999/bags',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'Test Bag'}
    )
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_create_bag_missing_name(client, db_session, auth_token, test_site):
    """Test POST /api/sites/<site_id>/bags with missing name returns 400"""
    response = client.post(f'/api/sites/{test_site.id}/bags',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'INVALID_INPUT'


def test_create_bag_client_cannot_provide_qr_token(client, db_session, auth_token, test_site):
    """Test POST rejects qr_token from client"""
    response = client.post(f'/api/sites/{test_site.id}/bags',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'name': 'Test Bag',
            'qr_token': 'client-provided-token'
        }
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'INVALID_INPUT'
    assert 'qr_token' in data['error']['message'].lower()


# List tests (2 tests)

def test_list_bags_by_site(client, db_session, auth_token, test_site):
    """Test GET /api/sites/<site_id>/bags returns bags for site"""
    # Create two bags
    bag1 = Bag(site_id=test_site.id, name='Bag 1', qr_token='token-1', active=True)
    bag2 = Bag(site_id=test_site.id, name='Bag 2', qr_token='token-2', active=False)
    db_session.add_all([bag1, bag2])
    db_session.commit()
    
    response = client.get(f'/api/sites/{test_site.id}/bags',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'bags' in data
    assert len(data['bags']) == 2
    # Verify both bags are present
    bag_names = [bag['name'] for bag in data['bags']]
    assert 'Bag 1' in bag_names
    assert 'Bag 2' in bag_names


def test_list_bags_invalid_site(client, db_session, auth_token):
    """Test GET /api/sites/<site_id>/bags for non-existent site returns 404"""
    response = client.get('/api/sites/9999/bags',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


# Get tests (2 tests)

def test_get_bag_success(client, db_session, auth_token, test_site):
    """Test GET /api/bags/<id> returns bag"""
    bag = Bag(site_id=test_site.id, name='Test Bag', qr_token='test-token-123', active=True)
    db_session.add(bag)
    db_session.commit()
    
    response = client.get(f'/api/bags/{bag.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == bag.id
    assert data['site_id'] == test_site.id
    assert data['name'] == 'Test Bag'
    assert data['qr_token'] == 'test-token-123'
    assert data['active'] is True


def test_get_bag_not_found(client, db_session, auth_token):
    """Test GET /api/bags/<id> returns 404 for non-existent bag"""
    response = client.get('/api/bags/9999',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


# Update tests (5 tests)

def test_update_bag_name(client, db_session, auth_token, test_site):
    """Test PATCH /api/bags/<id> updates name"""
    bag = Bag(site_id=test_site.id, name='Original Name', qr_token='test-token', active=True)
    db_session.add(bag)
    db_session.commit()
    bag_id = bag.id
    original_token = bag.qr_token
    
    response = client.patch(f'/api/bags/{bag_id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'Updated Name'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == bag_id
    assert data['name'] == 'Updated Name'
    assert data['qr_token'] == original_token  # qr_token unchanged
    assert data['active'] is True  # active unchanged
    assert data['updated_at'] is not None


def test_update_bag_active_status(client, db_session, auth_token, test_site):
    """Test PATCH /api/bags/<id> updates active status"""
    bag = Bag(site_id=test_site.id, name='Test Bag', qr_token='test-token', active=True)
    db_session.add(bag)
    db_session.commit()
    
    response = client.patch(f'/api/bags/{bag.id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'active': False}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['active'] is False
    assert data['name'] == 'Test Bag'  # name unchanged


def test_update_bag_not_found(client, db_session, auth_token):
    """Test PATCH /api/bags/<id> returns 404 for non-existent bag"""
    response = client.patch('/api/bags/9999',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'Updated Name'}
    )
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_update_bag_qr_token_immutable(client, db_session, auth_token, test_site):
    """Test PATCH rejects attempt to update qr_token"""
    bag = Bag(site_id=test_site.id, name='Test Bag', qr_token='original-token', active=True)
    db_session.add(bag)
    db_session.commit()
    
    response = client.patch(f'/api/bags/{bag.id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'qr_token': 'new-token'}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'INVALID_INPUT'
    assert 'immutable' in data['error']['message'].lower()


def test_update_bag_site_id_immutable(client, db_session, auth_token, test_site):
    """Test PATCH rejects attempt to update site_id"""
    bag = Bag(site_id=test_site.id, name='Test Bag', qr_token='test-token', active=True)
    db_session.add(bag)
    db_session.commit()
    
    response = client.patch(f'/api/bags/{bag.id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'site_id': 999}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'INVALID_INPUT'
    assert 'immutable' in data['error']['message'].lower()


# Delete tests (3 tests)

def test_delete_bag_success(client, db_session, auth_token, test_site):
    """Test DELETE /api/bags/<id> returns 204 when successful"""
    bag = Bag(site_id=test_site.id, name='Test Bag', qr_token='test-token', active=True)
    db_session.add(bag)
    db_session.commit()
    bag_id = bag.id
    
    response = client.delete(f'/api/bags/{bag_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 204
    assert response.data == b''  # Empty body
    
    # Verify bag is deleted
    deleted_bag = db_session.query(Bag).filter(Bag.id == bag_id).first()
    assert deleted_bag is None


def test_delete_bag_with_sessions_conflict(client, db_session, auth_token, test_site):
    """Test DELETE /api/bags/<id> returns 409 when bag has inventory sessions"""
    bag = Bag(site_id=test_site.id, name='Test Bag', qr_token='test-token', active=True)
    db_session.add(bag)
    db_session.commit()
    
    # Add an inventory session to the bag
    session = InventorySession(bag_id=bag.id)
    db_session.add(session)
    db_session.commit()
    
    response = client.delete(f'/api/bags/{bag.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'CONFLICT'
    assert 'inventory sessions' in data['error']['message'].lower()


def test_delete_bag_not_found(client, db_session, auth_token):
    """Test DELETE /api/bags/<id> returns 404 for non-existent bag"""
    response = client.delete('/api/bags/9999',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'
