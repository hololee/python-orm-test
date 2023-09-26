"""set default value to region

Revision ID: 5c545a0d9ee2
Revises: 6961f40870aa
Create Date: 2023-09-26 08:43:06.005757

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5c545a0d9ee2'
down_revision: Union[str, None] = '6961f40870aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'buckets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('name', sa.VARCHAR),
        sa.Column('mount', sa.Integer),
    )
    op.create_foreign_key(
        'users_bucket_fk',
        source_table='buckets',
        referent_schema='public',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint('users_bucket_fk', table_name='buckets')
    op.drop_table('buckets')
