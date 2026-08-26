"""add circles and community features
Revision ID: 20260827_circles
Revises: 20260826_mood_context
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "20260827_circles"
down_revision = "20260826_mood_context"
branch_labels = None
depends_on = None


def upgrade():
    # Circle model
    op.create_table(
        "circles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("topic", sa.String(100), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("max_participants", sa.Integer(), nullable=False, server_default=sa.text("25")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_circles_created_by_user_id", "circles", ["created_by_user_id"])

    # CircleMembership model
    op.create_table(
        "circle_memberships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("circle_id", sa.Integer(), sa.ForeignKey("circles.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("circle_id", "user_id", name="uq_circle_user"),
    )
    op.create_index("ix_circle_memberships_circle_id", "circle_memberships", ["circle_id"])
    op.create_index("ix_circle_memberships_user_id", "circle_memberships", ["user_id"])

    # CircleGathering model
    op.create_table(
        "circle_gatherings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("circle_id", sa.Integer(), sa.ForeignKey("circles.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("discussion_prompt", sa.Text()),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_circle_gatherings_circle_id", "circle_gatherings", ["circle_id"])

    # CircleMessage model
    op.create_table(
        "circle_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("gathering_id", sa.Integer(), sa.ForeignKey("circle_gatherings.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_circle_messages_gathering_id", "circle_messages", ["gathering_id"])
    op.create_index("ix_circle_messages_user_id", "circle_messages", ["user_id"])

    # CircleReaction model
    op.create_table(
        "circle_reactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("message_id", sa.Integer(), sa.ForeignKey("circle_messages.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("reaction_type", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("message_id", "user_id", "reaction_type", name="uq_circle_reaction"),
    )
    op.create_index("ix_circle_reactions_message_id", "circle_reactions", ["message_id"])

    # CircleReport model
    op.create_table(
        "circle_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("message_id", sa.Integer(), sa.ForeignKey("circle_messages.id"), nullable=False),
        sa.Column("reported_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("reason", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_circle_reports_message_id", "circle_reports", ["message_id"])


def downgrade():
    op.drop_index("ix_circle_reports_message_id", "circle_reports")
    op.drop_table("circle_reports")
    op.drop_index("ix_circle_reactions_message_id", "circle_reactions")
    op.drop_table("circle_reactions")
    op.drop_index("ix_circle_messages_user_id", "circle_messages")
    op.drop_index("ix_circle_messages_gathering_id", "circle_messages")
    op.drop_table("circle_messages")
    op.drop_index("ix_circle_gatherings_circle_id", "circle_gatherings")
    op.drop_table("circle_gatherings")
    op.drop_index("ix_circle_memberships_user_id", "circle_memberships")
    op.drop_index("ix_circle_memberships_circle_id", "circle_memberships")
    op.drop_table("circle_memberships")
    op.drop_index("ix_circles_created_by_user_id", "circles")
    op.drop_table("circles")
