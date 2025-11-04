import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_sensor(client: AsyncClient, sample_unit):
    """Test creating a sensor"""
    response = await client.post(
        "/api/v1/sensors/",
        json={
            "name": "Temperature Sensor",
            "sensor_type": "temperature",
            "unit_id": sample_unit["id"],
            "status": "active",
            "description": "Monitors room temperature"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Temperature Sensor"
    assert data["sensor_type"] == "temperature"
    assert data["unit_id"] == sample_unit["id"]
    assert "id" in data


@pytest.mark.asyncio
async def test_create_sensor_invalid_unit(client: AsyncClient):
    """Test creating a sensor with invalid unit_id"""
    response = await client.post(
        "/api/v1/sensors/",
        json={
            "name": "Test Sensor",
            "sensor_type": "temperature",
            "unit_id": 99999,
            "status": "active"
        }
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_sensor(client: AsyncClient, sample_sensor):
    """Test getting a sensor by ID"""
    response = await client.get(f"/api/v1/sensors/{sample_sensor['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_sensor["id"]


@pytest.mark.asyncio
async def test_get_all_sensors(client: AsyncClient):
    """Test getting all sensors"""
    response = await client.get("/api/v1/sensors/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_sensors_by_unit(client: AsyncClient, sample_unit, sample_sensor):
    """Test getting sensors filtered by unit_id"""
    response = await client.get(f"/api/v1/sensors/?unit_id={sample_unit['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(sensor["unit_id"] == sample_unit["id"] for sensor in data)


@pytest.mark.asyncio
async def test_update_sensor(client: AsyncClient, sample_sensor):
    """Test updating a sensor"""
    response = await client.put(
        f"/api/v1/sensors/{sample_sensor['id']}",
        json={
            "name": "Updated Sensor",
            "status": "inactive"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Sensor"
    assert data["status"] == "inactive"


@pytest.mark.asyncio
async def test_delete_sensor(client: AsyncClient, sample_unit):
    """Test deleting a sensor"""
    # Create a sensor first
    create_response = await client.post(
        "/api/v1/sensors/",
        json={
            "name": "Sensor to Delete",
            "sensor_type": "humidity",
            "unit_id": sample_unit["id"],
            "status": "active"
        }
    )
    sensor_id = create_response.json()["id"]
    
    # Delete it
    delete_response = await client.delete(f"/api/v1/sensors/{sensor_id}")
    assert delete_response.status_code == 200
    
    # Verify it's deleted
    get_response = await client.get(f"/api/v1/sensors/{sensor_id}")
    assert get_response.status_code == 404