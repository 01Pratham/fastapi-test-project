from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = 'c69f55ec846a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Add new columns
    op.add_column('tbl_users', sa.Column('created_date', sa.DateTime(timezone=True), server_default=func.now(), nullable=False))
    op.add_column('tbl_users', sa.Column('updated_date', sa.DateTime(timezone=True), onupdate=func.now(), nullable=True))
    op.add_column('tbl_users', sa.Column('is_deleted', sa.Boolean(), default=False, nullable=False))

def downgrade() -> None:
    # Remove the columns if rolling back
    op.drop_column('tbl_users', 'is_deleted')
    op.drop_column('tbl_users', 'updated_date')
    op.drop_column('tbl_users', 'created_date')
