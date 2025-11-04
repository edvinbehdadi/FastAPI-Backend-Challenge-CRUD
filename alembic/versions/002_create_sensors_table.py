"""create sensors table

Revision ID: 002
Revises: 001
Create Date: 2025-01-01 00:01:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE sensor_type_enum AS ENUM (
            'temperature', 'humidity', 'pressure', 'motion', 'light', 'other'
        );
        
        CREATE TYPE sensor_status_enum AS ENUM (
            'active', 'inactive', 'maintenance'
        );
        
        CREATE TABLE sensors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            sensor_type sensor_type_enum NOT NULL,
            unit_id INTEGER NOT NULL REFERENCES units(id) ON DELETE CASCADE,
            status sensor_status_enum NOT NULL DEFAULT 'active',
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX idx_sensors_unit_id ON sensors(unit_id);
        CREATE INDEX idx_sensors_type ON sensors(sensor_type);
        CREATE INDEX idx_sensors_status ON sensors(status);
        CREATE INDEX idx_sensors_created_at ON sensors(created_at);
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS sensors CASCADE;
        DROP TYPE IF EXISTS sensor_type_enum;
        DROP TYPE IF EXISTS sensor_status_enum;
    """)
