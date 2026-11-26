"""initial

Revision ID: 0001
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id"), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("comments")
    op.drop_table("posts")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
