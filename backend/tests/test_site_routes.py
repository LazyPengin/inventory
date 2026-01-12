"""
Tests for Site CRUD endpoints (BE-2)
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
from models import Admin, Site, Bag
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


def test_create_site_without_auth(client, db_session):
    """Test POST /api/sites without auth returns 401"""
    response = client.post('/api/sites', json={
        'name': 'Test Site',
        'alert_recipients': ['admin@example.com']
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_list_sites_without_auth(client, db_session):
    """Test GET /api/sites without auth returns 401"""
    response = client.get('/api/sites')
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_get_site_without_auth(client, db_session):
    """Test GET /api/sites/<id> without auth returns 401"""
    response = client.get('/api/sites/1')
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_update_site_without_auth(client, db_session):
    """Test PATCH /api/sites/<id> without auth returns 401"""
    response = client.patch('/api/sites/1', json={
        'name': 'Updated Site'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_delete_site_without_auth(client, db_session):
    """Test DELETE /api/sites/<id> without auth returns 401"""
    response = client.delete('/api/sites/1')
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'UNAUTHORIZED'


def test_create_site_success(client, db_session, auth_token):
    """Test POST /api/sites with valid data returns 201"""
    response = client.post('/api/sites', 
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'name': 'Main Office',
            'alert_recipients': ['admin@example.com', 'safety@example.com']
        }
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] is not None
    assert data['name'] == 'Main Office'
    assert data['alert_recipients'] == ['admin@example.com', 'safety@example.com']
    assert data['created_at'] is not None
    assert data['updated_at'] is None


def test_create_site_invalid_alert_recipients_not_array(client, db_session, auth_token):
    """Test POST /api/sites with invalid alert_recipients (not array) returns 400"""
    response = client.post('/api/sites',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'name': 'Test Site',
            'alert_recipients': 'not-an-array'
        }
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'INVALID_INPUT'
    assert 'must be a list' in data['error']['message']


def test_create_site_invalid_alert_recipients_no_at_sign(client, db_session, auth_token):
    """Test POST /api/sites with invalid email (no @) returns 400"""
    response = client.post('/api/sites',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'name': 'Test Site',
            'alert_recipients': ['invalid-email.com']
        }
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'INVALID_INPUT'
    assert '@' in data['error']['message'] or '.' in data['error']['message']


def test_create_site_missing_name(client, db_session, auth_token):
    """Test POST /api/sites with missing name returns 400"""
    response = client.post('/api/sites',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'alert_recipients': ['admin@example.com']
        }
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'INVALID_INPUT'


def test_list_sites_empty(client, db_session, auth_token):
    """Test GET /api/sites returns empty list when no sites"""
    response = client.get('/api/sites',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'sites' in data
    assert data['sites'] == []


def test_list_sites_with_data(client, db_session, auth_token):
    """Test GET /api/sites returns all sites"""
    # Create two sites
    alert_emails = json.dumps(['admin@example.com'])
    site1 = Site(name='Site 1', alert_recipients=alert_emails)
    site2 = Site(name='Site 2', alert_recipients=alert_emails)
    db_session.add_all([site1, site2])
    db_session.commit()
    
    response = client.get('/api/sites',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'sites' in data
    assert len(data['sites']) == 2
    # Check no bag_count in response
    for site in data['sites']:
        assert 'bag_count' not in site


def test_get_site_success(client, db_session, auth_token):
    """Test GET /api/sites/<id> returns site"""
    alert_emails = json.dumps(['admin@example.com'])
    site = Site(name='Test Site', alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    response = client.get(f'/api/sites/{site.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == site.id
    assert data['name'] == 'Test Site'
    assert data['alert_recipients'] == ['admin@example.com']
    # Check no bag_count in response
    assert 'bag_count' not in data


def test_get_site_not_found(client, db_session, auth_token):
    """Test GET /api/sites/<id> returns 404 for non-existent site"""
    response = client.get('/api/sites/9999',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_update_site_name(client, db_session, auth_token):
    """Test PATCH /api/sites/<id> updates site name"""
    alert_emails = json.dumps(['admin@example.com'])
    site = Site(name='Original Name', alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    site_id = site.id
    
    response = client.patch(f'/api/sites/{site_id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'Updated Name'}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == site_id
    assert data['name'] == 'Updated Name'
    assert data['alert_recipients'] == ['admin@example.com']  # Unchanged
    assert data['updated_at'] is not None


def test_update_site_alert_recipients(client, db_session, auth_token):
    """Test PATCH /api/sites/<id> updates alert_recipients"""
    alert_emails = json.dumps(['old@example.com'])
    site = Site(name='Test Site', alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    site_id = site.id
    
    response = client.patch(f'/api/sites/{site_id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'alert_recipients': ['new@example.com', 'admin@example.com']}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['alert_recipients'] == ['new@example.com', 'admin@example.com']
    assert data['name'] == 'Test Site'  # Unchanged


def test_update_site_not_found(client, db_session, auth_token):
    """Test PATCH /api/sites/<id> returns 404 for non-existent site"""
    response = client.patch('/api/sites/9999',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'name': 'Updated Name'}
    )
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'


def test_update_site_invalid_alert_recipients(client, db_session, auth_token):
    """Test PATCH /api/sites/<id> with invalid alert_recipients returns 400"""
    alert_emails = json.dumps(['admin@example.com'])
    site = Site(name='Test Site', alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    response = client.patch(f'/api/sites/{site.id}',
        headers={'Authorization': f'Bearer {auth_token}'},
        json={'alert_recipients': 'not-an-array'}
    )
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'INVALID_INPUT'


def test_delete_site_success(client, db_session, auth_token):
    """Test DELETE /api/sites/<id> returns 204 when successful"""
    alert_emails = json.dumps(['admin@example.com'])
    site = Site(name='Test Site', alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    site_id = site.id
    
    response = client.delete(f'/api/sites/{site_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 204
    assert response.data == b''  # Empty body
    
    # Verify site is deleted
    deleted_site = db_session.query(Site).filter(Site.id == site_id).first()
    assert deleted_site is None


def test_delete_site_with_bags_conflict(client, db_session, auth_token):
    """Test DELETE /api/sites/<id> returns 409 when site has bags"""
    alert_emails = json.dumps(['admin@example.com'])
    site = Site(name='Test Site', alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    # Add a bag to the site
    bag = Bag(site_id=site.id, name='Test Bag', qr_token='test-token-123', active=True)
    db_session.add(bag)
    db_session.commit()
    
    response = client.delete(f'/api/sites/{site.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'CONFLICT'
    assert 'bags' in data['error']['message'].lower()
    # Ensure no bag_count in error response
    assert 'bag_count' not in data
    assert 'bag_count' not in data['error']


def test_delete_site_not_found(client, db_session, auth_token):
    """Test DELETE /api/sites/<id> returns 404 for non-existent site"""
    response = client.delete('/api/sites/9999',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'
