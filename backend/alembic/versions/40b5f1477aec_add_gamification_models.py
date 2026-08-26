"""add gamification models

Revision ID: 40b5f1477aec
Revises: f944b5e406d1
Create Date: 2026-08-25 23:43:30.213217
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "40b5f1477aec"
down_revision: Union[str, Sequence[str], None] = "f944b5e406d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Achievements table
    op.create_table(
        "achievements",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.Column("points_required", sa.Integer(), nullable=False),
    )

    # User Achievements table
    op.create_table(
        "user_achievements",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("achievement_id", sa.Integer(), sa.ForeignKey("achievements.id"), nullable=False),
        sa.Column(
            "unlocked_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),
    )
    op.create_index("ix_user_achievements_user_id", "user_achievements", ["user_id"])
    op.create_index("ix_user_achievements_achievement_id", "user_achievements", ["achievement_id"])

    # User Gamification table
    op.create_table(
        "user_gamification",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("level", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("current_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("longest_streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_activity_date", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.create_index("ix_user_gamification_user_id", "user_gamification", ["user_id"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_user_gamification_user_id", table_name="user_gamification")
    op.drop_table("user_gamification")

    op.drop_index("ix_user_achievements_achievement_id", table_name="user_achievements")
    op.drop_index("ix_user_achievements_user_id", table_name="user_achievements")
    op.drop_table("user_achievements")

    op.drop_table("achievements")
