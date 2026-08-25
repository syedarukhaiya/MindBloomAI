"""add password hash to users

Revision ID: 869b59439c4c
Revises: 0979468c0b03
Create Date: 2026-08-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pwdlib import PasswordHash


revision: str = "869b59439c4c"
down_revision: Union[str, Sequence[str], None] = "0979468c0b03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    password_hash = PasswordHash.recommended()

    # Add the column temporarily as nullable so existing users can be updated.
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=True),
    )

    # Set a secure temporary password hash for existing development users.
    temporary_hash = password_hash.hash("ChangeMe123!")

    op.execute(
        sa.text(
            "UPDATE users SET password_hash = :password_hash "
            "WHERE password_hash IS NULL"
        ).bindparams(password_hash=temporary_hash)
    )

    # Now that every existing user has a hash, enforce NOT NULL.
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=False,
        )


def downgrade() -> None:
    op.drop_column("users", "password_hash")
