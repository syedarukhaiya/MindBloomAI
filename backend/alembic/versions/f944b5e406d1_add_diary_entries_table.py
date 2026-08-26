"""add diary entries table

Revision ID: f944b5e406d1
Revises: 869b59439c4c
Create Date: 2026-08-25 23:42:13.135682
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "f944b5e406d1"
down_revision: Union[str, Sequence[str], None] = "869b59439c4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "diary_entries",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("mood", sa.String(length=50), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.create_index("ix_diary_entries_user_id", "diary_entries", ["user_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_diary_entries_user_id", table_name="diary_entries")
    op.drop_table("diary_entries")
