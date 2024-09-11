"""Updated status to be a enum

Revision ID: 888e86e545d1
Revises: 
Create Date: 2024-09-11 00:44:24.730662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '888e86e545d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Enum('pending', 'active', 'finished', name='status_enum'),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.Enum('pending', 'active', 'finished', name='status_enum'),
               type_=sa.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###
