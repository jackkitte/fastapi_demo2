"""create_first_tables

Revision ID: 60dd74ca4fff
Revises: 
Create Date: 2021-12-07 22:33:39.205468+09:00
"""

import sqlalchemy as sa
from alembic import op

revision = "60dd74ca4fff"
down_revision = None
branch_labels = None
depends_on = None


def create_hedgehogs_table() -> None:
    op.create_table(
        "hedgehogs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("color_type", sa.Text, nullable=False),
        sa.Column("age", sa.Numeric(10, 2), nullable=False),
    )


def upgrade() -> None:
    create_hedgehogs_table()


def downgrade() -> None:
    pass
