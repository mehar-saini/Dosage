"""empty message

Revision ID: 66ac9c4e97de
Revises: 4682fb0caa9d
Create Date: 2020-06-05 20:24:25.927463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66ac9c4e97de'
down_revision = '4682fb0caa9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('hospital', sa.String(length=140), nullable=True),
    sa.Column('mrn', sa.String(length=20), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('bmi', sa.Float(), nullable=True),
    sa.Column('bsa', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mrn')
    )
    op.create_index(op.f('ix_patient_age'), 'patient', ['age'], unique=False)
    op.create_index(op.f('ix_patient_name'), 'patient', ['name'], unique=False)
    op.create_index(op.f('ix_patient_timestamp'), 'patient', ['timestamp'], unique=False)
    op.create_table('risk_factor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wbc', sa.Integer(), nullable=True),
    sa.Column('prednisolone', sa.String(length=10), nullable=True),
    sa.Column('tbd', sa.String(length=10), nullable=True),
    sa.Column('hrcyto', sa.String(length=10), nullable=True),
    sa.Column('cns', sa.String(length=10), nullable=True),
    sa.Column('acf', sa.String(length=10), nullable=True),
    sa.Column('risk_type', sa.String(length=10), nullable=True),
    sa.Column('mrd', sa.Float(), nullable=True),
    sa.Column('cr', sa.Float(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('patient_age', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_age'], ['patient.age'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_risk_factor_patient_id'), 'risk_factor', ['patient_id'], unique=False)
    op.create_index(op.f('ix_risk_factor_risk_type'), 'risk_factor', ['risk_type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_risk_factor_risk_type'), table_name='risk_factor')
    op.drop_index(op.f('ix_risk_factor_patient_id'), table_name='risk_factor')
    op.drop_table('risk_factor')
    op.drop_index(op.f('ix_patient_timestamp'), table_name='patient')
    op.drop_index(op.f('ix_patient_name'), table_name='patient')
    op.drop_index(op.f('ix_patient_age'), table_name='patient')
    op.drop_table('patient')
    # ### end Alembic commands ###
