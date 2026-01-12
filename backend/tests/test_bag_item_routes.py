"""
Tests for BagItem CRUD endpoints (BE-4)
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
from models import Admin, Site, Bag, BagItem, InventorySession, InventoryResult, InventoryStatus
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
def sample_site(db_session):
    """Create a sample site"""
    site = Site(name='Test Site', alert_recipients='["admin@example.com"]')
    db_session.add(site)
    db_session.commit()
    db_session.refresh(site)
    return site


@pytest.fixture
def sample_bag(db_session, sample_site):
    """Create a sample bag"""
    bag = Bag(
        site_id=sample_site.id,
        name='Test Bag',
        qr_token='test-token-123',
        active=True
    )
    db_session.add(bag)
    db_session.commit()
    db_session.refresh(bag)
    return bag


# Authentication tests

def test_create_item_without_auth(client, db_session, sample_bag):
    """POST /api/bags/:bag_id/items without auth returns 401"""
    response = client.post(f'/api/bags/{sample_bag.id}/items', json={
        'name': 'Test Item'
    })
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error']['code'] == 'UNAUTHORIZED'


# Create item tests

def test_create_item_success(client, auth_token, db_session, sample_bag):
    """POST /api/bags/:bag_id/items with valid data returns 201"""
    response = client.post(
        f'/api/bags/{sample_bag.id}/items',
        json={
            'name': 'Bandages',
            'expected_qty': 10,
            'track_expiry': True,
            'expiry_date': '2026-12-31',
            'test_batteries': False
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Bandages'
    assert data['bag_id'] == sample_bag.id
    assert data['expected_qty'] == 10
    assert data['track_expiry'] is True
    assert data['expiry_date'] == '2026-12-31'
    assert data['test_batteries'] is False
    assert 'id' in data
    assert 'created_at' in data


def test_create_item_missing_name(client, auth_token, db_session, sample_bag):
    """POST /api/bags/:bag_id/items without name returns 400"""
    response = client.post(
        f'/api/bags/{sample_bag.id}/items',
        json={'expected_qty': 5},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error']['code'] == 'INVALID_INPUT'
    assert 'name' in data['error']['message'].lower()


def test_create_item_negative_qty(client, auth_token, db_session, sample_bag):
    """POST /api/bags/:bag_id/items with negative qty returns 400"""
    response = client.post(
        f'/api/bags/{sample_bag.id}/items',
        json={
            'name': 'Test Item',
            'expected_qty': -5
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error']['code'] == 'INVALID_INPUT'
    assert 'expected_qty' in data['error']['message'].lower()


def test_create_item_expiry_date_without_track_expiry(client, auth_token, db_session, sample_bag):
    """POST /api/bags/:bag_id/items with expiry_date but track_expiry=false returns 400"""
    response = client.post(
        f'/api/bags/{sample_bag.id}/items',
        json={
            'name': 'Test Item',
            'track_expiry': False,
            'expiry_date': '2026-12-31'
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error']['code'] == 'INVALID_INPUT'
    assert 'track_expiry' in data['error']['message'].lower()


def test_create_item_invalid_bag(client, auth_token, db_session):
    """POST /api/bags/:bag_id/items with invalid bag_id returns 404"""
    response = client.post(
        '/api/bags/99999/items',
        json={'name': 'Test Item'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error']['code'] == 'NOT_FOUND'


def test_create_item_with_null_qty(client, auth_token, db_session, sample_bag):
    """POST /api/bags/:bag_id/items with expected_qty=null (presence-only) returns 201"""
    response = client.post(
        f'/api/bags/{sample_bag.id}/items',
        json={
            'name': 'First Aid Manual',
            'expected_qty': None,
            'track_expiry': False,
            'test_batteries': False
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'First Aid Manual'
    assert data['expected_qty'] is None


def test_create_item_with_expiry_tracking(client, auth_token, db_session, sample_bag):
    """POST /api/bags/:bag_id/items with track_expiry=true and expiry_date returns 201"""
    response = client.post(
        f'/api/bags/{sample_bag.id}/items',
        json={
            'name': 'Antiseptic Wipes',
            'expected_qty': 20,
            'track_expiry': True,
            'expiry_date': '2027-03-15'
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['track_expiry'] is True
    assert data['expiry_date'] == '2027-03-15'


def test_create_item_with_test_batteries(client, auth_token, db_session, sample_bag):
    """POST /api/bags/:bag_id/items with test_batteries=true returns 201"""
    response = client.post(
        f'/api/bags/{sample_bag.id}/items',
        json={
            'name': 'Flashlight',
            'test_batteries': True
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['test_batteries'] is True


# List items tests

def test_list_items_for_bag(client, auth_token, db_session, sample_bag):
    """GET /api/bags/:bag_id/items returns items for bag"""
    # Create two items
    item1 = BagItem(bag_id=sample_bag.id, name='Item 1', expected_qty=5)
    item2 = BagItem(bag_id=sample_bag.id, name='Item 2', expected_qty=None)
    db_session.add_all([item1, item2])
    db_session.commit()
    
    response = client.get(
        f'/api/bags/{sample_bag.id}/items',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) == 2
    assert data['items'][0]['name'] == 'Item 1'
    assert data['items'][1]['name'] == 'Item 2'


def test_list_items_invalid_bag(client, auth_token, db_session):
    """GET /api/bags/:bag_id/items for non-existent bag returns 404"""
    response = client.get(
        '/api/bags/99999/items',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error']['code'] == 'NOT_FOUND'


# Get item tests

def test_get_item_by_id(client, auth_token, db_session, sample_bag):
    """GET /api/items/:id returns item data"""
    from datetime import date
    item = BagItem(
        bag_id=sample_bag.id,
        name='Test Item',
        expected_qty=10,
        track_expiry=True,
        expiry_date=date(2026, 12, 31)
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response = client.get(
        f'/api/items/{item.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == item.id
    assert data['name'] == 'Test Item'
    assert data['expected_qty'] == 10


def test_get_item_not_found(client, auth_token, db_session):
    """GET /api/items/:id for non-existent item returns 404"""
    response = client.get(
        '/api/items/99999',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error']['code'] == 'NOT_FOUND'


# Update item tests

def test_update_item_success(client, auth_token, db_session, sample_bag):
    """PATCH /api/items/:id updates fields"""
    item = BagItem(bag_id=sample_bag.id, name='Old Name', expected_qty=5)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response = client.patch(
        f'/api/items/{item.id}',
        json={
            'name': 'New Name',
            'expected_qty': 10,
            'test_batteries': True
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'New Name'
    assert data['expected_qty'] == 10
    assert data['test_batteries'] is True
    assert 'updated_at' in data
    assert data['updated_at'] is not None


def test_update_item_immutable_bag_id(client, auth_token, db_session, sample_bag):
    """PATCH /api/items/:id attempting to change bag_id returns 400"""
    item = BagItem(bag_id=sample_bag.id, name='Test Item')
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response = client.patch(
        f'/api/items/{item.id}',
        json={'bag_id': 999},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error']['code'] == 'INVALID_INPUT'
    assert 'immutable' in data['error']['message'].lower()


def test_update_item_not_found(client, auth_token, db_session):
    """PATCH /api/items/:id for non-existent item returns 404"""
    response = client.patch(
        '/api/items/99999',
        json={'name': 'New Name'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error']['code'] == 'NOT_FOUND'


def test_update_item_clear_expiry_date(client, auth_token, db_session, sample_bag):
    """PATCH /api/items/:id to clear expiry_date (set to null) returns 200"""
    from datetime import date
    item = BagItem(
        bag_id=sample_bag.id,
        name='Test Item',
        track_expiry=True,
        expiry_date=date(2026, 12, 31)
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response = client.patch(
        f'/api/items/{item.id}',
        json={
            'track_expiry': False,
            'expiry_date': None
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['track_expiry'] is False
    assert data['expiry_date'] is None


# Delete item tests

def test_delete_item_success(client, auth_token, db_session, sample_bag):
    """DELETE /api/items/:id returns 204"""
    item = BagItem(bag_id=sample_bag.id, name='Test Item')
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    response = client.delete(
        f'/api/items/{item.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 204
    
    # Verify item is deleted
    deleted_item = db_session.query(BagItem).filter(BagItem.id == item.id).first()
    assert deleted_item is None


def test_delete_item_not_found(client, auth_token, db_session):
    """DELETE /api/items/:id for non-existent item returns 404"""
    response = client.delete(
        '/api/items/99999',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error']['code'] == 'NOT_FOUND'


def test_delete_item_with_results_succeeds(client, auth_token, db_session, sample_bag):
    """
    DELETE /api/items/:id succeeds even if inventory_results exist.
    Per DB-1 schema: bag_item_id has ON DELETE SET NULL.
    """
    # Create item
    item = BagItem(bag_id=sample_bag.id, name='Test Item')
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    # Create inventory session
    session = InventorySession(bag_id=sample_bag.id)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    
    # Create inventory result linked to item
    result = InventoryResult(
        session_id=session.id,
        bag_item_id=item.id,
        status=InventoryStatus.PRESENT
    )
    db_session.add(result)
    db_session.commit()
    
    # Delete item should succeed (SET NULL on result.bag_item_id)
    response = client.delete(
        f'/api/items/{item.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 204
    
    # Verify item is deleted
    deleted_item = db_session.query(BagItem).filter(BagItem.id == item.id).first()
    assert deleted_item is None
    
    # Verify result still exists with bag_item_id set to NULL
    db_session.refresh(result)
    assert result.bag_item_id is None
