"""merging two heads

Revision ID: cf2492bccadd
Revises: 25c5b630f2fc, 691c89104572
Create Date: 2023-03-27 16:02:20.846376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf2492bccadd'
down_revision = ('25c5b630f2fc', '691c89104572')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
