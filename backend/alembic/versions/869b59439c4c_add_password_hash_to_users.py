"""add password hash to users

Revision ID: 869b59439c4c
Revises: 0979468c0b03
Create Date: 2026-08-25
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = "869b59439c4c"
down_revision: Union[str, Sequence[str], None] = "0979468c0b03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Add column as nullable
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=True),
    )

    # Step 2: Backfill existing rows with a temporary secure hash
    temporary_hash = (
        "$argon2id$v=19$m=65536,t=3,p=4$IfY3GaRIfVuv7KnXEYxgqw$hbww92FWqpkWvwEUcrnsJP4bQQ3ZtvQ3Y0OlM33Z4LU"
    )
    op.execute(
        sa.text("UPDATE users SET password_hash = :password_hash WHERE password_hash IS NULL").bindparams(
            password_hash=temporary_hash
        )
    )

    # Step 3: Enforce NOT NULL
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=False,
        )


def downgrade() -> None:
    op.drop_column("users", "password_hash")
