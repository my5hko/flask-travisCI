"""empty message

Revision ID: 726318cbebbc
Revises: 
Create Date: 2024-12-24 15:42:01.845448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '726318cbebbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_expense_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_expense'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense')
    op.drop_table('user')
    # ### end Alembic commands ###
