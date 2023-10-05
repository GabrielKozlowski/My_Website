"""same error with heads

Revision ID: 6f9e5c765372
Revises: 1921fc7b170c, 73c51496dc88
Create Date: 2023-04-04 14:30:39.075983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f9e5c765372'
down_revision = ('1921fc7b170c', '73c51496dc88')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
