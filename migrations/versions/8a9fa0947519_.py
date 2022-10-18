"""empty message

Revision ID: 8a9fa0947519
Revises: c9fe770652d0
Create Date: 2022-08-31 13:32:53.340667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a9fa0947519'
down_revision = 'c9fe770652d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('start_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'start_time')
    # ### end Alembic commands ###