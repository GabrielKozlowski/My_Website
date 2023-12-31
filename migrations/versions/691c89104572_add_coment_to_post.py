"""add coment to post

Revision ID: 691c89104572
Revises: aaaac03d61d0
Create Date: 2023-03-23 13:41:54.902146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '691c89104572'
down_revision = 'aaaac03d61d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=200), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('poster_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['poster_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('poster_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['poster_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['poster_id'], ['id'])
        batch_op.alter_column('poster_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    op.drop_table('comment')
    # ### end Alembic commands ###
