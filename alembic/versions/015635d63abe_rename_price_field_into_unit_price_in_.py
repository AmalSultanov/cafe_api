"""Rename price field into unit_price in cart_items table

Revision ID: 015635d63abe
Revises: fd468fc42b66
Create Date: 2025-07-20 11:27:31.916728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '015635d63abe'
down_revision: Union[str, None] = 'fd468fc42b66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_items', sa.Column('unit_price', sa.Numeric(), nullable=True))
    op.drop_column('cart_items', 'price')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_items', sa.Column('price', sa.NUMERIC(), autoincrement=False, nullable=True))
    op.drop_column('cart_items', 'unit_price')
    # ### end Alembic commands ###
