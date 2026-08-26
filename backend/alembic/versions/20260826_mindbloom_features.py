"""mindbloom wellbeing feature set
Revision ID: 20260826_mb
Revises: 9d4f6c8a7b1e
"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = "20260826_mb"
down_revision = "9d4f6c8a7b1e"
branch_labels = None
depends_on = None


def upgrade():
    # Conversations
    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("listener_mode", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("language", sa.String(30), nullable=False, server_default="English"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_conversations_user_id", "conversations", ["user_id"])

    # Messages
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("risk_level", sa.String(20), nullable=False, server_default="NORMAL"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_messages_conversation_id", "messages", ["conversation_id"])

    # Other wellbeing-related tables
    op.create_table(
        "ai_memory",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("memory", sa.Text(), nullable=False),
        sa.Column("source", sa.String(50), nullable=False, server_default="user_approved"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

    op.create_table(
        "user_preferences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("language", sa.String(30), nullable=False, server_default="English"),
        sa.Column("tone", sa.String(30), nullable=False, server_default="warm"),
        sa.Column("memory_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("reminders_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("quiet_hours", sa.String(30)),
    )

    op.create_table(
        "trusted_contacts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("relation", sa.String(60), nullable=False),
        sa.Column("phone", sa.String(40)),
        sa.Column("email", sa.String(255)),
        sa.Column("consent_to_share", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    op.create_table(
        "safety_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("risk_level", sa.String(20), nullable=False),
        sa.Column("source", sa.String(30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

    op.create_table(
        "wellbeing_activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(100), unique=True, nullable=False),
        sa.Column("title", sa.String(150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(60), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=False, server_default="60"),
    )

    op.create_table(
        "activity_completions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("activity_id", sa.Integer(), sa.ForeignKey("wellbeing_activities.id"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

    op.create_table(
        "support_resources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("category", sa.String(80), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("url", sa.String(500)),
        sa.Column("phone", sa.String(60)),
        sa.Column("language", sa.String(50), nullable=False, server_default="English"),
        sa.Column("location", sa.String(120)),
        sa.Column("verified", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("demo_only", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    # Seed wellbeing activities
    op.execute(
        """
        INSERT INTO wellbeing_activities (slug,title,description,category,duration_seconds)
        VALUES
        ('one_minute_reset','60-second reset','Slow your breathing: inhale gently, pause, and make the exhale a little longer.','mindfulness',60),
        ('brain_dump','One-minute brain dump','Write every thought down without organizing it.','reflection',60),
        ('study_reset','15-minute study reset','Choose one tiny study task and work only on that task for 15 minutes.','study',900),
        ('grounding','5-4-3-2-1 grounding','Notice 5 things you see, 4 you feel, 3 you hear, 2 you smell, and 1 you taste.','grounding',180)
        """
    )

    # Seed support resources
    op.execute(
        """
        INSERT INTO support_resources (name,category,description,language,verified,demo_only)
        VALUES
        ('Emergency services','emergency','For immediate danger, contact your local emergency service or go to the nearest emergency department.','English',true,false)
        """
    )


def downgrade():
    for t in [
        "support_resources",
        "activity_completions",
        "wellbeing_activities",
        "safety_events",
        "trusted_contacts",
        "user_preferences",
        "ai_memory",
        "messages",
        "conversations",
    ]:
        op.drop_table(t)
