"""add content column to posts table

Revision ID: bdd4357c064d
Revises: f4725806d4fe
Create Date: 2024-08-27 15:45:10.729287

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bdd4357c064d"
down_revision: Union[str, None] = "f4725806d4fe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
