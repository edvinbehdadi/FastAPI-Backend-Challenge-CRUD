import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_sensor_data(client: AsyncClient, sample_sensor):
    """Test creating sensor data"""
    response = await client.post(
        "/api/v1/sensor-data/",
        json={
            "sensor_id": sample_sensor["id"],
            "value": 23.5,
            "unit": "celsius",
            "status": "pending"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["sensor_id"] == sample_sensor["id"]
    assert data["value"] == 23.5
    assert data["status"] == "pending"
    assert "id" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_create_sensor_data_invalid_sensor(client: AsyncClient):
    """Test creating sensor data with invalid sensor_id"""
    response = await client.post(
        "/api/v1/sensor-data/",
        json={
            "sensor_id": 99999,
            "value": 23.5,
            "unit": "celsius"
        }
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_sensor_data(client: AsyncClient, sample_sensor_data):
    """Test getting sensor data by ID"""
    response = await client.get(f"/api/v1/sensor-data/{sample_sensor_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_sensor_data["id"]


@pytest.mark.asyncio
async def test_get_all_sensor_data(client: AsyncClient):
    """Test getting all sensor data"""
    response = await client.get("/api/v1/sensor-data/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_sensor_data_by_sensor(client: AsyncClient, sample_sensor, sample_sensor_data):
    """Test getting sensor data filtered by sensor_id"""
    response = await client.get(f"/api/v1/sensor-data/?sensor_id={sample_sensor['id']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(item["sensor_id"] == sample_sensor["id"] for item in data)


@pytest.mark.asyncio
async def test_get_sensor_data_by_status(client: AsyncClient, sample_sensor_data):
    """Test getting sensor data filtered by status"""
    response = await client.get("/api/v1/sensor-data/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_sensor_data_with_details(client: AsyncClient, sample_sensor_data):
    """Test getting sensor data with details"""
    response = await client.get("/api/v1/sensor-data/?with_details=true")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "sensor_name" in data[0]
        assert "sensor_type" in data[0]
        assert "unit_name" in data[0]


@pytest.mark.asyncio
async def test_update_sensor_data(client: AsyncClient, sample_sensor_data):
    """Test updating sensor data"""
    response = await client.put(
        f"/api/v1/sensor-data/{sample_sensor_data['id']}",
        json={
            "value": 27.3,
            "status": "validated"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 27.3
    assert data["status"] == "validated"


@pytest.mark.asyncio
async def test_validate_sensor_data(client: AsyncClient, sample_sensor):
    """Test validating sensor data"""
    # Create sensor data first
    create_response = await client.post(
        "/api/v1/sensor-data/",
        json={
            "sensor_id": sample_sensor["id"],
            "value": 20.0,
            "unit": "celsius",
            "status": "pending"
        }
    )
    data_id = create_response.json()["id"]
    
    # Validate it
    response = await client.put(f"/api/v1/sensor-data/{data_id}/validate")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "validated"


@pytest.mark.asyncio
async def test_archive_sensor_data(client: AsyncClient, sample_sensor):
    """Test archiving sensor data"""
    # Create sensor data first
    create_response = await client.post(
        "/api/v1/sensor-data/",
        json={
            "sensor_id": sample_sensor["id"],
            "value": 21.0,
            "unit": "celsius",
            "status": "validated"
        }
    )
    data_id = create_response.json()["id"]
    
    # Archive it
    response = await client.put(f"/api/v1/sensor-data/{data_id}/archive")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "archived"


@pytest.mark.asyncio
async def test_delete_sensor_data(client: AsyncClient, sample_sensor):
    """Test deleting sensor data"""
    # Create sensor data first
    create_response = await client.post(
        "/api/v1/sensor-data/",
        json={
            "sensor_id": sample_sensor["id"],
            "value": 22.0,
            "unit": "celsius"
        }
    )
    data_id = create_response.json()["id"]
    
    # Delete it
    delete_response = await client.delete(f"/api/v1/sensor-data/{data_id}")
    assert delete_response.status_code == 200
    
    # Verify it's deleted
    get_response = await client.get(f"/api/v1/sensor-data/{data_id}")
    assert get_response.status_code == 404