"""create contractors table

Revision ID: 9a007eeecfa1
Revises: 
Create Date: 2025-01-19 21:04:39.283104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a007eeecfa1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("contractors",
                    sa.Column('company_id', sa.Integer, primary_key=True),
                    sa.Column('company_name', sa.String(255), nullable=False),
                    sa.Column('company_website', sa.String(255), nullable=False),
                    sa.Column('company_type', sa.String(255), nullable=False),
                    sa.Column('company_province', sa.String(255), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table("contractors")
