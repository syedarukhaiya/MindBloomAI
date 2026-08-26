"""add mood context fields
Revision ID: 20260826_moodctx
Revises: 20260826_mb
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "20260826_moodctx"
down_revision = "20260826_mb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("mood_entries", sa.Column("stress", sa.Integer(), nullable=True))
    op.add_column("mood_entries", sa.Column("energy", sa.Integer(), nullable=True))
    op.add_column("mood_entries", sa.Column("context", sa.String(length=200), nullable=True))


def downgrade() -> None:
    op.drop_column("mood_entries", "context")
    op.drop_column("mood_entries", "energy")
    op.drop_column("mood_entries", "stress")
