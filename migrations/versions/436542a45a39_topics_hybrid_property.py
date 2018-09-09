"""topics hybrid property

Revision ID: 436542a45a39
Revises: cb476761f410
Create Date: 2018-09-08 19:55:22.114799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '436542a45a39'
down_revision = 'cb476761f410'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.create_foreign_key('user_foreign_key', 'users', ['create_uid'], ['id'])

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topics', schema=None) as batch_op:
        batch_op.drop_constraint('user_foreign_key', type_='foreignkey')

    # ### end Alembic commands ###