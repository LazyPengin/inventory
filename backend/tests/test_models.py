"""
Tests for database models (DB-1)
Tests model imports, CRUD operations, FK behavior, and qr_token queries
"""
import pytest
import os
import sys
import json
from pathlib import Path
from datetime import date

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test database
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['TESTING'] = 'true'

from database import Base, engine, SessionLocal
from models import Site, Bag, BagItem, InventorySession, InventoryResult, InventoryStatus


@pytest.fixture
def db_session():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_import_models():
    """Test that all models can be imported"""
    assert Site is not None
    assert Bag is not None
    assert BagItem is not None
    assert InventorySession is not None
    assert InventoryResult is not None
    assert InventoryStatus is not None


def test_create_site(db_session):
    """Test creating a site"""
    alert_emails = json.dumps(["admin@example.com", "safety@example.com"])
    site = Site(name="Main Office", alert_recipients=alert_emails)
    
    db_session.add(site)
    db_session.commit()
    
    assert site.id is not None
    assert site.name == "Main Office"
    assert site.alert_recipients == alert_emails
    assert site.created_at is not None


def test_create_bag_with_qr_token(db_session):
    """Test creating a bag with unique qr_token"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag = Bag(
        site_id=site.id,
        name="First Aid Kit",
        qr_token="test-token-12345",
        active=True
    )
    db_session.add(bag)
    db_session.commit()
    
    assert bag.id is not None
    assert bag.qr_token == "test-token-12345"
    assert bag.active is True


def test_bag_qr_token_unique_constraint(db_session):
    """Test that qr_token must be unique"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag1 = Bag(site_id=site.id, name="Bag 1", qr_token="duplicate-token", active=True)
    db_session.add(bag1)
    db_session.commit()
    
    # Try to create another bag with same qr_token
    bag2 = Bag(site_id=site.id, name="Bag 2", qr_token="duplicate-token", active=True)
    db_session.add(bag2)
    
    with pytest.raises(Exception):  # IntegrityError
        db_session.commit()


def test_query_bag_by_qr_token(db_session):
    """Test querying bag by qr_token (no performance assertion per C/REVIEW)"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    # Create multiple bags
    for i in range(5):
        bag = Bag(
            site_id=site.id,
            name=f"Bag {i}",
            qr_token=f"token-{i:04d}",
            active=True
        )
        db_session.add(bag)
    db_session.commit()
    
    # Query by qr_token
    found_bag = db_session.query(Bag).filter(Bag.qr_token == "token-0002").first()
    
    assert found_bag is not None
    assert found_bag.name == "Bag 2"
    assert found_bag.qr_token == "token-0002"


def test_create_bag_items(db_session):
    """Test creating bag items with various configurations"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag = Bag(site_id=site.id, name="Safety Kit", qr_token="test-token", active=True)
    db_session.add(bag)
    db_session.commit()
    
    # Item with expected quantity
    item1 = BagItem(
        bag_id=bag.id,
        name="Bandages",
        expected_qty=10,
        track_expiry=False,
        test_batteries=False
    )
    
    # Item with presence-only check (expected_qty=NULL)
    item2 = BagItem(
        bag_id=bag.id,
        name="First Aid Manual",
        expected_qty=None,  # Presence-only check
        track_expiry=False,
        test_batteries=False
    )
    
    # Item with expiry tracking
    item3 = BagItem(
        bag_id=bag.id,
        name="Antiseptic Wipes",
        expected_qty=5,
        track_expiry=True,
        expiry_date=date(2026, 12, 31),
        test_batteries=False
    )
    
    # Item requiring battery test
    item4 = BagItem(
        bag_id=bag.id,
        name="Flashlight",
        expected_qty=1,
        track_expiry=False,
        test_batteries=True
    )
    
    db_session.add_all([item1, item2, item3, item4])
    db_session.commit()
    
    assert item1.expected_qty == 10
    assert item2.expected_qty is None  # Presence-only
    assert item3.track_expiry is True
    assert item4.test_batteries is True


def test_create_inventory_session(db_session):
    """Test creating an inventory session"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag = Bag(site_id=site.id, name="Test Bag", qr_token="test-token", active=True)
    db_session.add(bag)
    db_session.commit()
    
    session = InventorySession(
        bag_id=bag.id,
        nickname="John Doe",
        ip_address="192.168.1.100",
        geo_city="Montreal",
        geo_country="Canada"
    )
    db_session.add(session)
    db_session.commit()
    
    assert session.id is not None
    assert session.bag_id == bag.id
    assert session.nickname == "John Doe"
    assert session.created_at is not None


def test_create_inventory_results(db_session):
    """Test creating inventory results with different statuses"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag = Bag(site_id=site.id, name="Test Bag", qr_token="test-token", active=True)
    db_session.add(bag)
    db_session.commit()
    
    item1 = BagItem(bag_id=bag.id, name="Item 1", expected_qty=10)
    item2 = BagItem(bag_id=bag.id, name="Item 2", expected_qty=5)
    db_session.add_all([item1, item2])
    db_session.commit()
    
    session = InventorySession(bag_id=bag.id)
    db_session.add(session)
    db_session.commit()
    
    # Test all status types
    result1 = InventoryResult(
        session_id=session.id,
        bag_item_id=item1.id,
        status=InventoryStatus.PRESENT,
        observed_qty=10
    )
    
    result2 = InventoryResult(
        session_id=session.id,
        bag_item_id=item2.id,
        status=InventoryStatus.NOT_ENOUGH,
        observed_qty=3,
        notes="Found only 3 instead of 5"
    )
    
    db_session.add_all([result1, result2])
    db_session.commit()
    
    assert result1.status == InventoryStatus.PRESENT
    assert result2.status == InventoryStatus.NOT_ENOUGH
    assert result2.observed_qty == 3


def test_foreign_key_cascade_bag_to_items(db_session):
    """Test CASCADE: deleting bag deletes its items"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag = Bag(site_id=site.id, name="Test Bag", qr_token="test-token", active=True)
    db_session.add(bag)
    db_session.commit()
    
    item = BagItem(bag_id=bag.id, name="Test Item", expected_qty=1)
    db_session.add(item)
    db_session.commit()
    
    item_id = item.id
    
    # Delete bag (should cascade to items)
    db_session.delete(bag)
    db_session.commit()
    
    # Verify item was deleted
    deleted_item = db_session.query(BagItem).filter(BagItem.id == item_id).first()
    assert deleted_item is None


def test_foreign_key_restrict_site_to_bags(db_session):
    """Test RESTRICT: cannot delete site with existing bags"""
    from sqlalchemy.exc import IntegrityError
    
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag = Bag(site_id=site.id, name="Test Bag", qr_token="test-token", active=True)
    db_session.add(bag)
    db_session.commit()
    
    # Try to delete site (should fail due to RESTRICT)
    db_session.delete(site)
    
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_foreign_key_cascade_session_to_results(db_session):
    """Test CASCADE: deleting session deletes its results"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag = Bag(site_id=site.id, name="Test Bag", qr_token="test-token", active=True)
    db_session.add(bag)
    db_session.commit()
    
    session = InventorySession(bag_id=bag.id)
    db_session.add(session)
    db_session.commit()
    
    result = InventoryResult(
        session_id=session.id,
        status=InventoryStatus.PRESENT
    )
    db_session.add(result)
    db_session.commit()
    
    result_id = result.id
    
    # Delete session (should cascade to results)
    db_session.delete(session)
    db_session.commit()
    
    # Verify result was deleted
    deleted_result = db_session.query(InventoryResult).filter(InventoryResult.id == result_id).first()
    assert deleted_result is None


def test_foreign_key_set_null_item_to_results(db_session):
    """Test SET NULL: deleting bag_item sets bag_item_id to NULL in results"""
    alert_emails = json.dumps(["admin@example.com"])
    site = Site(name="Test Site", alert_recipients=alert_emails)
    db_session.add(site)
    db_session.commit()
    
    bag = Bag(site_id=site.id, name="Test Bag", qr_token="test-token", active=True)
    db_session.add(bag)
    db_session.commit()
    
    item = BagItem(bag_id=bag.id, name="Test Item", expected_qty=1)
    db_session.add(item)
    db_session.commit()
    
    session = InventorySession(bag_id=bag.id)
    db_session.add(session)
    db_session.commit()
    
    result = InventoryResult(
        session_id=session.id,
        bag_item_id=item.id,
        status=InventoryStatus.PRESENT
    )
    db_session.add(result)
    db_session.commit()
    
    result_id = result.id
    
    # Delete item (should set bag_item_id to NULL in result)
    db_session.delete(item)
    db_session.commit()
    
    # Verify result still exists but bag_item_id is NULL
    updated_result = db_session.query(InventoryResult).filter(InventoryResult.id == result_id).first()
    assert updated_result is not None
    assert updated_result.bag_item_id is None
