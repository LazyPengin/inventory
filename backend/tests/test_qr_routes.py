"""
Tests for QR lookup endpoint (BE-5)
Public (anonymous) endpoint - no authentication required
"""
import pytest
import os
import sys
import json
from pathlib import Path
from datetime import date

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ['JWT_SECRET'] = 'test-secret-key-for-testing'
os.environ['ADMIN_PASSWORD'] = 'testpassword123'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['TESTING'] = 'true'

from app import app
from database import Base, engine, SessionLocal
from models import Site, Bag, BagItem


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
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_site(db_session):
    """Create a sample site"""
    site = Site(name='Test Site', alert_recipients='["admin@example.com"]')
    db_session.add(site)
    db_session.commit()
    db_session.refresh(site)
    return site


@pytest.fixture
def active_bag_with_items(db_session, sample_site):
    """Create an active bag with items"""
    bag = Bag(
        site_id=sample_site.id,
        name='Emergency Kit',
        qr_token='test-token-active',
        active=True
    )
    db_session.add(bag)
    db_session.commit()
    db_session.refresh(bag)
    
    # Add items
    item1 = BagItem(
        bag_id=bag.id,
        name='Bandages',
        expected_qty=10,
        track_expiry=True,
        expiry_date=date(2026, 12, 31),
        test_batteries=False
    )
    item2 = BagItem(
        bag_id=bag.id,
        name='Flashlight',
        expected_qty=1,
        track_expiry=False,
        expiry_date=None,
        test_batteries=True
    )
    db_session.add_all([item1, item2])
    db_session.commit()
    
    return bag


@pytest.fixture
def active_bag_no_items(db_session, sample_site):
    """Create an active bag with no items"""
    bag = Bag(
        site_id=sample_site.id,
        name='Empty Bag',
        qr_token='test-token-empty',
        active=True
    )
    db_session.add(bag)
    db_session.commit()
    db_session.refresh(bag)
    return bag


@pytest.fixture
def inactive_bag(db_session, sample_site):
    """Create an inactive bag"""
    bag = Bag(
        site_id=sample_site.id,
        name='Inactive Bag',
        qr_token='test-token-inactive',
        active=False
    )
    db_session.add(bag)
    db_session.commit()
    db_session.refresh(bag)
    return bag


# Success tests

def test_lookup_valid_bag_with_items(client, db_session, active_bag_with_items):
    """GET /api/qr/<qr_token> with valid token returns 200 with bag and items"""
    response = client.get('/api/qr/test-token-active')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    
    # Verify bag structure
    assert 'bag' in data
    assert data['bag']['id'] == active_bag_with_items.id
    assert data['bag']['site_id'] == active_bag_with_items.site_id
    assert data['bag']['name'] == 'Emergency Kit'
    assert data['bag']['active'] is True
    
    # Verify items structure
    assert 'items' in data
    assert len(data['items']) == 2
    
    # Verify first item
    assert data['items'][0]['name'] == 'Bandages'
    assert data['items'][0]['expected_qty'] == 10
    assert data['items'][0]['track_expiry'] is True
    assert data['items'][0]['expiry_date'] == '2026-12-31'
    assert data['items'][0]['test_batteries'] is False
    
    # Verify second item
    assert data['items'][1]['name'] == 'Flashlight'
    assert data['items'][1]['expected_qty'] == 1
    assert data['items'][1]['track_expiry'] is False
    assert data['items'][1]['expiry_date'] is None
    assert data['items'][1]['test_batteries'] is True


def test_lookup_valid_bag_no_items(client, db_session, active_bag_no_items):
    """GET /api/qr/<qr_token> with valid token but no items returns 200 with empty items array"""
    response = client.get('/api/qr/test-token-empty')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    
    # Verify bag
    assert 'bag' in data
    assert data['bag']['name'] == 'Empty Bag'
    assert data['bag']['active'] is True
    
    # Verify empty items array
    assert 'items' in data
    assert data['items'] == []
    assert len(data['items']) == 0


# Error tests

def test_lookup_invalid_token(client, db_session):
    """GET /api/qr/<qr_token> with non-existent token returns 404"""
    response = client.get('/api/qr/invalid-token-xyz')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'
    assert 'not found' in data['error']['message'].lower()


def test_lookup_inactive_bag(client, db_session, inactive_bag):
    """GET /api/qr/<qr_token> with inactive bag returns 404 (not 403, to avoid info leakage)"""
    response = client.get('/api/qr/test-token-inactive')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error']['code'] == 'NOT_FOUND'
    assert 'not found' in data['error']['message'].lower()


# Response shape and security tests

def test_response_shape_completeness(client, db_session, active_bag_with_items):
    """Verify response contains all required fields"""
    response = client.get('/api/qr/test-token-active')
    data = json.loads(response.data)
    
    # Bag fields
    required_bag_fields = ['id', 'site_id', 'name', 'active']
    for field in required_bag_fields:
        assert field in data['bag'], f"Missing bag field: {field}"
    
    # Items fields (if items exist)
    if data['items']:
        required_item_fields = ['id', 'name', 'expected_qty', 'track_expiry', 
                               'expiry_date', 'test_batteries', 'created_at']
        for field in required_item_fields:
            assert field in data['items'][0], f"Missing item field: {field}"


def test_qr_token_not_in_response(client, db_session, active_bag_with_items):
    """Verify qr_token is NOT exposed in response (security check)"""
    response = client.get('/api/qr/test-token-active')
    data = json.loads(response.data)
    
    # Ensure qr_token is not in bag object
    assert 'qr_token' not in data['bag']
    
    # Convert response to string and check it doesn't contain the token
    response_str = json.dumps(data)
    assert 'test-token-active' not in response_str


def test_items_ordered_by_created_at(client, db_session, sample_site):
    """Verify items are ordered by created_at"""
    import time
    
    # Create bag
    bag = Bag(
        site_id=sample_site.id,
        name='Test Bag',
        qr_token='test-token-order',
        active=True
    )
    db_session.add(bag)
    db_session.commit()
    db_session.refresh(bag)
    
    # Add items with slight delay to ensure different timestamps
    item1 = BagItem(bag_id=bag.id, name='First Item', expected_qty=1)
    db_session.add(item1)
    db_session.commit()
    
    time.sleep(0.01)  # Small delay
    
    item2 = BagItem(bag_id=bag.id, name='Second Item', expected_qty=2)
    db_session.add(item2)
    db_session.commit()
    
    time.sleep(0.01)  # Small delay
    
    item3 = BagItem(bag_id=bag.id, name='Third Item', expected_qty=3)
    db_session.add(item3)
    db_session.commit()
    
    # Look up bag
    response = client.get('/api/qr/test-token-order')
    data = json.loads(response.data)
    
    # Verify order
    assert len(data['items']) == 3
    assert data['items'][0]['name'] == 'First Item'
    assert data['items'][1]['name'] == 'Second Item'
    assert data['items'][2]['name'] == 'Third Item'


def test_multiple_items_all_returned(client, db_session, sample_site):
    """Verify all items are returned for a bag with multiple items"""
    # Create bag with 5 items
    bag = Bag(
        site_id=sample_site.id,
        name='Multi-Item Bag',
        qr_token='test-token-multi',
        active=True
    )
    db_session.add(bag)
    db_session.commit()
    db_session.refresh(bag)
    
    # Add 5 items
    for i in range(1, 6):
        item = BagItem(
            bag_id=bag.id,
            name=f'Item {i}',
            expected_qty=i
        )
        db_session.add(item)
    db_session.commit()
    
    # Look up bag
    response = client.get('/api/qr/test-token-multi')
    data = json.loads(response.data)
    
    # Verify all items returned
    assert len(data['items']) == 5
    for i in range(5):
        assert data['items'][i]['name'] == f'Item {i+1}'
        assert data['items'][i]['expected_qty'] == i+1


def test_no_authentication_required(client, db_session, active_bag_with_items):
    """Verify endpoint works without authentication (public endpoint)"""
    # No Authorization header provided
    response = client.get('/api/qr/test-token-active')
    
    # Should succeed (not 401)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'bag' in data
    assert 'items' in data
