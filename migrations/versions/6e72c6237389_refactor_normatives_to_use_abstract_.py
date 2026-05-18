"""refactor normatives to use abstract base class

Revision ID: 6e72c6237389
Revises: 668a123638b3
Create Date: 2026-05-17 20:21:58.388977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6e72c6237389'
down_revision: Union[str, Sequence[str], None] = '668a123638b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Apaga o índice antigo associado ao nome da tabela antiga
    op.drop_index('ix_normatives_id', table_name='normatives')
    
    # 2. Renomeia a tabela que já tem os dados (normatives -> bcb_normatives)
    op.rename_table('normatives', 'bcb_normatives')
    
    # 3. Cria o novo índice para a tabela agora renomeada
    op.create_index(op.f('ix_bcb_normatives_id'), 'bcb_normatives', ['id'], unique=False)

    # 4. Cria a tabela de CVM (esta realmente precisa ser criada do zero)
    op.create_table('cvm_normatives',
        sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('normative_type', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cvm_normatives_id'), 'cvm_normatives', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Apaga a tabela CVM que foi recém-criada
    op.drop_index(op.f('ix_cvm_normatives_id'), table_name='cvm_normatives')
    op.drop_table('cvm_normatives')

    # 2. Desfaz a renomeação (bcb_normatives -> normatives)
    op.drop_index(op.f('ix_bcb_normatives_id'), table_name='bcb_normatives')
    op.rename_table('bcb_normatives', 'normatives')
    op.create_index(op.f('ix_normatives_id'), 'normatives', ['id'], unique=False)
    # ### end Alembic commands ###
