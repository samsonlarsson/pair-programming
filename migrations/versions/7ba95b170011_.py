"""empty message

Revision ID: 7ba95b170011
Revises: 54a025d9cc54
Create Date: 2016-03-29 16:45:50.189830

"""

# revision identifiers, used by Alembic.
revision = '7ba95b170011'
down_revision = '54a025d9cc54'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_name', sa.String(length=250), nullable=True),
    sa.Column('session_address', sa.String(length=250), nullable=True),
    sa.Column('session_lang', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('unions',
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('unions')
    op.drop_table('sessions')
    ### end Alembic commands ###
