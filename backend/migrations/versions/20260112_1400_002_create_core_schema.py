"""create_core_schema

Revision ID: 002
Revises: 001
Create Date: 2026-01-12 14:00:00.000000

Creates core tables for QR Inventory MVP:
- sites: Physical locations
- bags: Bags/kits with QR codes
- bag_items: Expected items in bags (Note: table name deviation from tasks.md approved)
- inventory_sessions: Inventory check events
- inventory_results: Item status in inventory checks

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create core schema tables"""
    
    # Create sites table
    op.create_table(
        'sites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('alert_recipients', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sites_id'), 'sites', ['id'], unique=False)
    
    # Create bags table
    op.create_table(
        'bags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('site_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('qr_token', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('qr_token')
    )
    op.create_index(op.f('ix_bags_id'), 'bags', ['id'], unique=False)
    op.create_index(op.f('ix_bags_qr_token'), 'bags', ['qr_token'], unique=True)
    
    # Create bag_items table (approved deviation: 'bag_items' instead of 'items')
    op.create_table(
        'bag_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bag_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('expected_qty', sa.Integer(), nullable=True),
        sa.Column('track_expiry', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('test_batteries', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['bag_id'], ['bags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bag_items_id'), 'bag_items', ['id'], unique=False)
    
    # Create inventory_sessions table
    op.create_table(
        'inventory_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bag_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.Column('nickname', sa.String(length=255), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('geo_city', sa.String(length=255), nullable=True),
        sa.Column('geo_country', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['bag_id'], ['bags.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_sessions_id'), 'inventory_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_inventory_sessions_created_at'), 'inventory_sessions', ['created_at'], unique=False)
    
    # Create inventory_results table
    op.create_table(
        'inventory_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('bag_item_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('PRESENT', 'MISSING', 'NOT_ENOUGH', 'BATTERY_LOW', name='inventorystatus'), nullable=False),
        sa.Column('observed_qty', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['inventory_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['bag_item_id'], ['bag_items.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_results_id'), 'inventory_results', ['id'], unique=False)


def downgrade() -> None:
    """Drop core schema tables in reverse order"""
    op.drop_index(op.f('ix_inventory_results_id'), table_name='inventory_results')
    op.drop_table('inventory_results')
    
    op.drop_index(op.f('ix_inventory_sessions_created_at'), table_name='inventory_sessions')
    op.drop_index(op.f('ix_inventory_sessions_id'), table_name='inventory_sessions')
    op.drop_table('inventory_sessions')
    
    op.drop_index(op.f('ix_bag_items_id'), table_name='bag_items')
    op.drop_table('bag_items')
    
    op.drop_index(op.f('ix_bags_qr_token'), table_name='bags')
    op.drop_index(op.f('ix_bags_id'), table_name='bags')
    op.drop_table('bags')
    
    op.drop_index(op.f('ix_sites_id'), table_name='sites')
    op.drop_table('sites')
