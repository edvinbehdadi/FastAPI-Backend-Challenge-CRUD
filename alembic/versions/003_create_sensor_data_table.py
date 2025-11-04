"""create sensor_data table

Revision ID: 003
Revises: 002
Create Date: 2025-01-01 00:02:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE data_status_enum AS ENUM (
            'pending', 'validated', 'archived', 'invalid'
        );
        
        CREATE TABLE sensor_data (
            id SERIAL PRIMARY KEY,
            sensor_id INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
            value DOUBLE PRECISION NOT NULL,
            unit VARCHAR(50),
            status data_status_enum NOT NULL DEFAULT 'pending',
            timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX idx_sensor_data_sensor_id ON sensor_data(sensor_id);
        CREATE INDEX idx_sensor_data_status ON sensor_data(status);
        CREATE INDEX idx_sensor_data_timestamp ON sensor_data(timestamp);
        CREATE INDEX idx_sensor_data_sensor_timestamp ON sensor_data(sensor_id, timestamp DESC);
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS sensor_data CASCADE;
        DROP TYPE IF EXISTS data_status_enum;
    """)
