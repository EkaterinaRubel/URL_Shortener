"""url_mapping__creaded

Revision ID: 412ca968a108
Revises: 
Create Date: 2023-11-24 10:35:51.363612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '412ca968a108'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_mapping',
    sa.Column('url_id', sa.BigInteger(), nullable=False),
    sa.Column('short_url', sa.String(), nullable=False),
    sa.Column('long_url', sa.String(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('click_count', sa.BigInteger(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('url_id')
    )
    op.create_index(op.f('ix_url_mapping_short_url'), 'url_mapping', ['short_url'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_url_mapping_short_url'), table_name='url_mapping')
    op.drop_table('url_mapping')
    # ### end Alembic commands ###
