"""First migration

Revision ID: 9845428e2f66
Revises: 
Create Date: 2023-06-15 21:08:39.338195

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9845428e2f66"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currencies",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("create_date", sa.TIMESTAMP(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="derbit",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("currencies", schema="derbit")
    # ### end Alembic commands ###