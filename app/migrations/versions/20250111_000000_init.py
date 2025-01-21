"""Initial tables

Revision ID: 20250111_000000_init
Revises: 
Create Date: 2025-01-11 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = '20250111_000000_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'buildings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('activities.id')),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('building_id', sa.Integer(), sa.ForeignKey('buildings.id')),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'organization_phones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('organization_id', sa.Integer(),
                  sa.ForeignKey('organizations.id')),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'organization_activity',
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id']),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id']),
        sa.PrimaryKeyConstraint('organization_id', 'activity_id')
    )


def downgrade():
    op.drop_table('organization_activity')
    op.drop_table('organization_phones')
    op.drop_table('organizations')
    op.drop_table('activities')
    op.drop_table('buildings')
