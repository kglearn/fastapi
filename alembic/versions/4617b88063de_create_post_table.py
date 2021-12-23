"""create post table

Revision ID: 4617b88063de
Revises: 
Create Date: 2021-12-23 17:17:34.389027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4617b88063de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
