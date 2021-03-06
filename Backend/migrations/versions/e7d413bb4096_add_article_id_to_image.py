"""Add article id to image

Revision ID: e7d413bb4096
Revises: aa0800002c0d
Create Date: 2020-05-06 15:10:24.316043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7d413bb4096'
down_revision = 'aa0800002c0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('article_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'images', 'articles', ['article_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.drop_column('images', 'article_id')
    # ### end Alembic commands ###
