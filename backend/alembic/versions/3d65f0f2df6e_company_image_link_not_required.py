"""company_image_link_not_required

Revision ID: 3d65f0f2df6e
Revises: b223064efbd7
Create Date: 2024-08-17 22:40:57.395155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d65f0f2df6e'
down_revision: Union[str, None] = 'b223064efbd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('company', 'image_link',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('company', 'image_link',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
