"""add personal reflection features
Revision ID: 20260827_personal_reflection
Revises: 20260827_stories
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "20260827_personal_reflection"
down_revision = "20260827_stories"
branch_labels = None
depends_on = None


def upgrade():
    # FutureLetter model
    op.create_table(
        "future_letters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("recipient", sa.String(100), nullable=False, server_default="My Future Self"),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_sent", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_future_letters_user_id", "future_letters", ["user_id"])

    # GratitudeCapsule model
    op.create_table(
        "gratitude_capsules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("media_url", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_gratitude_capsules_user_id", "gratitude_capsules", ["user_id"])

    # SmallWin model
    op.create_table(
        "small_wins",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("is_anonymous", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("visibility", sa.String(20), nullable=False, server_default="PRIVATE"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_small_wins_user_id", "small_wins", ["user_id"])

    # KindnessMessage model
    op.create_table(
        "kindness_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("from_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("to_user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("is_anonymous", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_kindness_messages_from_user_id", "kindness_messages", ["from_user_id"])
    op.create_index("ix_kindness_messages_to_user_id", "kindness_messages", ["to_user_id"])

    # MemoryGarden model
    op.create_table(
        "memory_gardens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("bloom_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("growth_stage", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("last_growth_update", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_memory_gardens_user_id", "memory_gardens", ["user_id"])

    # ReflectionPrompt model
    op.create_table(
        "reflection_prompts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("language", sa.String(30), nullable=False, server_default="English"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )


def downgrade():
    op.drop_table("reflection_prompts")
    op.drop_index("ix_memory_gardens_user_id", "memory_gardens")
    op.drop_table("memory_gardens")
    op.drop_index("ix_kindness_messages_to_user_id", "kindness_messages")
    op.drop_index("ix_kindness_messages_from_user_id", "kindness_messages")
    op.drop_table("kindness_messages")
    op.drop_index("ix_small_wins_user_id", "small_wins")
    op.drop_table("small_wins")
    op.drop_index("ix_gratitude_capsules_user_id", "gratitude_capsules")
    op.drop_table("gratitude_capsules")
    op.drop_index("ix_future_letters_user_id", "future_letters")
    op.drop_table("future_letters")
