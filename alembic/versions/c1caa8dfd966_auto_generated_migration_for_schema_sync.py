"""Auto-generated migration for schema sync

Revision ID: c1caa8dfd966
Revises: b2b9f5b432ed
Create Date: 2023-12-30 19:17:42.510851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1caa8dfd966'
down_revision: Union[str, None] = 'b2b9f5b432ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###
