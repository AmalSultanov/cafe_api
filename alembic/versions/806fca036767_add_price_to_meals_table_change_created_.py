"""add price to meals table, change created_at

Revision ID: 806fca036767
Revises: 3d67aa08acf8
Create Date: 2025-04-06 17:21:19.607100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '806fca036767'
down_revision: Union[str, None] = '3d67aa08acf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meals', sa.Column('price', sa.Numeric(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meals', 'price')
    # ### end Alembic commands ###
