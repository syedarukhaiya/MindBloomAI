"""add story garden and community sharing features
Revision ID: 20260827_stories
Revises: 20260827_circles
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "20260827_stories"
down_revision = "20260827_circles"
branch_labels = None
depends_on = None


def upgrade():
    # Story model
    op.create_table(
        "stories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("is_anonymous", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_approved", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_stories_user_id", "stories", ["user_id"])

    # StoryReaction model
    op.create_table(
        "story_reactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("story_id", sa.Integer(), sa.ForeignKey("stories.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("reaction_type", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("story_id", "user_id", "reaction_type", name="uq_story_reaction"),
    )
    op.create_index("ix_story_reactions_story_id", "story_reactions", ["story_id"])

    # StoryReport model
    op.create_table(
        "story_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("story_id", sa.Integer(), sa.ForeignKey("stories.id"), nullable=False),
        sa.Column("reported_by_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("reason", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_story_reports_story_id", "story_reports", ["story_id"])


def downgrade():
    op.drop_index("ix_story_reports_story_id", "story_reports")
    op.drop_table("story_reports")
    op.drop_index("ix_story_reactions_story_id", "story_reactions")
    op.drop_table("story_reactions")
    op.drop_index("ix_stories_user_id", "stories")
    op.drop_table("stories")
