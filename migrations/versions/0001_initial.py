from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_table("plants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("species", sa.String(100)),
        sa.Column("room", sa.String(100)),
        sa.Column("watering_interval", sa.Integer(), nullable=False, server_default="7"),
        sa.Column("last_watered", sa.Date()),
        sa.Column("notes", sa.Text()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False))
    op.create_index("ix_plants_owner_id", "plants", ["owner_id"])
    op.create_table("waterings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("watered_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("amount_ml", sa.Integer(), nullable=False, server_default="200"),
        sa.Column("fertilizer_used", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("note", sa.String(300)),
        sa.Column("plant_id", sa.Integer(), sa.ForeignKey("plants.id"), nullable=False))
    op.create_index("ix_waterings_plant_id", "waterings", ["plant_id"])

def downgrade():
    op.drop_index("ix_waterings_plant_id", table_name="waterings")
    op.drop_table("waterings")
    op.drop_index("ix_plants_owner_id", table_name="plants")
    op.drop_table("plants")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
