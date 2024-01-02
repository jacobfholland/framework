"""Auto-generated migration for schema sync

Revision ID: eb0b2dcaa2a8
Revises: 434d5003e52b
Create Date: 2024-01-02 02:06:30.553816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb0b2dcaa2a8'
down_revision: Union[str, None] = '434d5003e52b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie')
    op.drop_table('user')
    op.drop_table('group')
    op.drop_table('permission_group')
    op.drop_table('permission')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('model', sa.VARCHAR(), nullable=True),
    sa.Column('model_get', sa.BOOLEAN(), nullable=True),
    sa.Column('model_create', sa.BOOLEAN(), nullable=True),
    sa.Column('model_update', sa.BOOLEAN(), nullable=True),
    sa.Column('model_delete', sa.BOOLEAN(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('deleted_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission_group',
    sa.Column('group_id', sa.INTEGER(), nullable=True),
    sa.Column('permission_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], )
    )
    op.create_table('group',
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('deleted_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('password', sa.VARCHAR(), nullable=True),
    sa.Column('avatar', sa.VARCHAR(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('deleted_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movie',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('deleted_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
