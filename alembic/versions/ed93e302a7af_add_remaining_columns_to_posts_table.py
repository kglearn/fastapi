"""add remaining columns to posts table

Revision ID: ed93e302a7af
Revises: b0f0dabeedf3
Create Date: 2021-12-23 17:53:01.158913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed93e302a7af'
down_revision = 'b0f0dabeedf3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('votes', sa.Integer(), nullable=False, server_default="0"))
    op.add_column('posts', sa.Column('createdAt', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column('ownerId', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['ownerId'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'votes')
    op.drop_column('posts', 'createdAt')
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'ownerId')
    pass
