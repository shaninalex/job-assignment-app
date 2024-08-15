"""initial

Revision ID: 45ea224cc4ff
Revises: 
Create Date: 2024-08-15 07:26:05.844907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '45ea224cc4ff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accounts')
    op.drop_table('auth')
    op.drop_table('admin_staff')
    op.drop_table('staff')
    op.drop_table('company')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='company_pkey'),
    sa.UniqueConstraint('name', name='company_name_key')
    )
    op.create_table('staff',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='staff_pkey'),
    sa.UniqueConstraint('email', name='staff_email_key'),
    sa.UniqueConstraint('name', name='staff_name_key'),
    sa.UniqueConstraint('password', name='staff_password_key')
    )
    op.create_table('admin_staff',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='admin_staff_pkey'),
    sa.UniqueConstraint('email', name='admin_staff_email_key'),
    sa.UniqueConstraint('name', name='admin_staff_name_key'),
    sa.UniqueConstraint('password', name='admin_staff_password_key')
    )
    op.create_table('auth',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('hash', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('ACTIVE', 'BANNED', 'PENDING', name='authstatus'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='auth_pkey'),
    sa.UniqueConstraint('email', name='auth_email_key'),
    sa.UniqueConstraint('hash', name='auth_hash_key')
    )
    op.create_table('accounts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='accounts_pkey'),
    sa.UniqueConstraint('name', name='accounts_name_key')
    )
    # ### end Alembic commands ###
