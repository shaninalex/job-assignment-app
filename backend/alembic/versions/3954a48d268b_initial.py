"""initial

Revision ID: 3954a48d268b
Revises: 
Create Date: 2024-08-24 18:35:25.562682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3954a48d268b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_staff',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('company',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('image_link', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    sa.Column('settings', sa.JSON(), nullable=True),
    sa.Column('active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('social_accounts', sa.JSON(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'BANNED', 'PENDING', name='authstatus'), nullable=False),
    sa.Column('role', sa.Enum('CANDIDATE', 'COMPANY_MEMBER', 'COMPANY_ADMIN', name='role'), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('candidate',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('resume_link', sa.Text(), nullable=True),
    sa.Column('social_accounts', sa.JSON(), nullable=True),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('about_additional', sa.Text(), nullable=True),
    sa.Column('skills', sa.JSON(), nullable=True),
    sa.Column('certificates', sa.JSON(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('company_manager',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('company_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('confirm_codes',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    sa.Column('code', sa.VARCHAR(length=6), nullable=False),
    sa.Column('status', sa.Enum('CREATED', 'SENT', 'USED', name='confirmstatuscode'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('expired_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('candidate_experience',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('company_name', sa.Text(), nullable=True),
    sa.Column('company_link', sa.Text(), nullable=True),
    sa.Column('work_start', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('work_end', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('position', sa.Text(), nullable=True),
    sa.Column('responsibility', sa.Text(), nullable=True),
    sa.Column('candidate_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidate.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('candidate_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candidate_experience')
    op.drop_table('confirm_codes')
    op.drop_table('company_manager')
    op.drop_table('candidate')
    op.drop_table('user')
    op.drop_table('company')
    op.drop_table('admin_staff')
    # ### end Alembic commands ###
