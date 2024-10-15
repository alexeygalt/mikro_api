"""access field removed

Revision ID: 21bca6d33c4e
Revises: 316aeafe7051
Create Date: 2024-10-15 09:26:35.954459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21bca6d33c4e'
down_revision: Union[str, None] = '316aeafe7051'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserProfile', 'access_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserProfile', sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###