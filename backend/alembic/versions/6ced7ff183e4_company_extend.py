"""company_extend

Revision ID: 6ced7ff183e4
Revises: 905f96ic6e965
Create Date: 2024-10-07 02:49:56.472521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6ced7ff183e4'
down_revision: Union[str, None] = '905f96c6e965'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('company', sa.Column('website', sa.VARCHAR(length=100), nullable=False))
    op.add_column('company', sa.Column('email', sa.VARCHAR(length=100), nullable=False))


def downgrade() -> None:
    op.drop_column('company', 'websites')
    op.drop_column('company', 'email')

