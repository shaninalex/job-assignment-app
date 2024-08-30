"""position_price_range

Revision ID: ecedbd5cc8b1
Revises: 03fe2c8830c8
Create Date: 2024-08-24 22:59:34.238281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecedbd5cc8b1'
down_revision: Union[str, None] = '03fe2c8830c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('positions', sa.Column('price_range', sa.VARCHAR(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('positions', 'price_range')
    # ### end Alembic commands ###