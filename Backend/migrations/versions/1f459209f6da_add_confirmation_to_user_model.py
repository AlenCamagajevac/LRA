"""Add confirmation to user model

Revision ID: 1f459209f6da
Revises: c4b66e2bafde
Create Date: 2020-02-29 08:44:09.364723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f459209f6da'
down_revision = 'c4b66e2bafde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('users', sa.Column('confirmed_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed_date')
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###