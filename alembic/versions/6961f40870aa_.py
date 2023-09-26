"""empty message

Revision ID: 6961f40870aa
Revises:
Create Date: 2023-09-26 08:40:50.250199

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6961f40870aa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 마이그레이션시 수행.
    op.add_column('users', sa.Column('region', sa.VARCHAR))


def downgrade() -> None:
    # 롤백시 수행.
    op.drop_column('users', 'region')
