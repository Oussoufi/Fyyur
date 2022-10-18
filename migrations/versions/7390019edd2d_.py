"""empty message

Revision ID: 7390019edd2d
Revises: 5b49e9c410ad
Create Date: 2022-08-31 02:48:58.392610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7390019edd2d'
down_revision = '5b49e9c410ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('start_time', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'start_time')
    # ### end Alembic commands ###
