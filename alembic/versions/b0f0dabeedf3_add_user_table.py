"""add user table

Revision ID: b0f0dabeedf3
Revises: 4f330171cfd2
Create Date: 2021-12-23 17:43:05.330791

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.util.compat import u


# revision identifiers, used by Alembic.
revision = 'b0f0dabeedf3'
down_revision = '4f330171cfd2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                             sa.Column('email', sa.String(), nullable=False, unique=True),
                             sa.Column('password', sa.String(), nullable=False),
                             sa.Column('createdAt', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                             sa.PrimaryKeyConstraint('id'),
                             sa.UniqueConstraint('email')
    
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
