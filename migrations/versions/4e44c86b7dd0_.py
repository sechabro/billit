"""empty message

Revision ID: 4e44c86b7dd0
Revises: 9023d6a0b834
Create Date: 2022-06-15 09:08:26.290656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e44c86b7dd0'
down_revision = '9023d6a0b834'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('clients',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company', sa.Text(), nullable=False),
    sa.Column('contact', sa.String(length=128), nullable=False),
    sa.Column('address', sa.Text(), nullable=False),
    sa.Column('city', sa.String(length=128), nullable=False),
    sa.Column('state', sa.String(length=128), nullable=False),
    sa.Column('zipcode', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('paid', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['client'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('invoices')
    op.drop_table('clients')
