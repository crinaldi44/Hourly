"""Migration

Revision ID: 7483185dd655
Revises: 0c5383b8fdc7
Create Date: 2023-02-12 07:55:06.009855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7483185dd655'
down_revision = '0c5383b8fdc7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clockins', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'clockins', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clockins', type_='foreignkey')
    op.drop_column('clockins', 'user_id')
    # ### end Alembic commands ###
