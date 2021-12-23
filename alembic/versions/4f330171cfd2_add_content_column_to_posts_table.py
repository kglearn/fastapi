"""add content column to posts table

Revision ID: 4f330171cfd2
Revises: 4617b88063de
Create Date: 2021-12-23 17:36:31.788391

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import String


# revision identifiers, used by Alembic.
revision = '4f330171cfd2'
down_revision = '4617b88063de'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
