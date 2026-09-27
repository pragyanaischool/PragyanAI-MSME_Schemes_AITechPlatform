"""initial_tables

Revision ID: 0001_initial_tables
Revises: 
Create Date: 2026-03-30 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("jurisdiction", sa.String(length=50), nullable=False, server_default="Karnataka"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("udyam_reg_no", sa.String(length=50), nullable=False, unique=True),
        sa.Column("gstn", sa.String(length=15), nullable=False, unique=True),
        sa.Column("state", sa.String(length=50), nullable=False, server_default="Karnataka"),
        sa.Column("district", sa.String(length=50), nullable=False),
        sa.Column("zone", sa.String(length=50), nullable=False, server_default="Zone 2 (Developing)"),
        sa.Column("sector", sa.String(length=50), nullable=False),
        sa.Column("turnover_lakhs", sa.Float(), nullable=False),
        sa.Column("plant_machinery_inv_lakhs", sa.Float(), nullable=False),
        sa.Column("employees", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_woman_owned", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("verification_status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(op.f("ix_companies_gstn"), "companies", ["gstn"], unique=True)
    op.create_index(op.f("ix_companies_udyam_reg_no"), "companies", ["udyam_reg_no"], unique=True)

    op.create_table(
        "schemes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("level", sa.String(length=20), nullable=False, server_default="State"),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("subsidy_percentage", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("max_cap_lakhs", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("target_sector", sa.JSON(), nullable=False),
        sa.Column("required_documents", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.create_index(op.f("ix_schemes_code"), "schemes", ["code"], unique=True)

    op.create_table(
        "applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("scheme_code", sa.String(length=50), nullable=False),
        sa.Column("current_stage", sa.String(length=50), nullable=False, server_default="Submitted"),
        sa.Column("claimed_amount_lakhs", sa.Float(), nullable=False),
        sa.Column("sanctioned_amount_lakhs", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("attached_documents", sa.JSON(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table("applications")
    op.drop_table("schemes")
    op.drop_table("companies")
    op.drop_table("users")
