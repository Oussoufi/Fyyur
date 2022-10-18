"""empty message

Revision ID: c9fe770652d0
Revises: 7390019edd2d
Create Date: 2022-08-31 02:50:13.266722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9fe770652d0'
down_revision = '7390019edd2d'
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
