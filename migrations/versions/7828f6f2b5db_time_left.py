"""time left

Revision ID: 7828f6f2b5db
Revises: 436542a45a39
Create Date: 2018-09-12 17:04:05.636798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7828f6f2b5db'
down_revision = '436542a45a39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.add_column(sa.Column('close_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('create_uid', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('user_foreign_key','users', ['create_uid'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('create_uid')
        batch_op.drop_column('close_date')

    # ### end Alembic commands ###