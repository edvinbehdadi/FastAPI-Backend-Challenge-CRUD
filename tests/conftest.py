import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import DatabasePool


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Setup and teardown database for each test"""
    # Create pool before each test
    await DatabasePool.create_pool()
    yield
    # Close pool after each test
    await DatabasePool.close_pool()


@pytest.fixture
async def client():
    """Create test client"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def sample_unit(client):
    """Create a sample unit for testing"""
    response = await client.post(
        "/api/v1/units/",
        json={
            "name": "Test Unit",
            "location": "Test Location",
            "description": "Test Description"
        }
    )
    return response.json()


@pytest.fixture
async def sample_sensor(client, sample_unit):
    """Create a sample sensor for testing"""
    response = await client.post(
        "/api/v1/sensors/",
        json={
            "name": "Test Sensor",
            "sensor_type": "temperature",
            "unit_id": sample_unit["id"],
            "status": "active",
            "description": "Test Sensor Description"
        }
    )
    return response.json()


@pytest.fixture
async def sample_sensor_data(client, sample_sensor):
    """Create a sample sensor data for testing"""
    response = await client.post(
        "/api/v1/sensor-data/",
        json={
            "sensor_id": sample_sensor["id"],
            "value": 25.5,
            "unit": "celsius",
            "status": "pending"
        }
    )
    return response.json()