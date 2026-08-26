"""add mood entries and reminders

Revision ID: 9d4f6c8a7b1e
Revises: 40b5f1477aec
Create Date: 2026-08-26
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "9d4f6c8a7b1e"
down_revision: Union[str, Sequence[str], None] = "40b5f1477aec"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Mood Entries Table
    op.create_table(
        "mood_entries",
        sa.Column("id", sa.Integer(), primary_key=True, index=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("mood", sa.String(length=50), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_mood_entries_user_id", "mood_entries", ["user_id"])

    # Reminders Table
    op.create_table(
        "reminders",
        sa.Column("id", sa.Integer(), primary_key=True, index=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("reminder_time", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_reminders_user_id", "reminders", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_reminders_user_id", table_name="reminders")
    op.drop_table("reminders")

    op.drop_index("ix_mood_entries_user_id", table_name="mood_entries")
    op.drop_table("mood_entries")
