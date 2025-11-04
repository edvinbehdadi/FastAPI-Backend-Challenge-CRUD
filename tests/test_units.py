import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_unit(client: AsyncClient):
    """Test creating a unit"""
    response = await client.post(
        "/api/v1/units/",
        json={
            "name": "Factory A",
            "location": "Building 1, Floor 2",
            "description": "Main production unit"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Factory A"
    assert data["location"] == "Building 1, Floor 2"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_unit(client: AsyncClient, sample_unit):
    """Test getting a unit by ID"""
    response = await client.get(f"/api/v1/units/{sample_unit['id']}")  
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_unit["id"]
    assert data["name"] == sample_unit["name"]


@pytest.mark.asyncio
async def test_get_unit_not_found(client: AsyncClient):
    """Test getting a non-existent unit"""
    response = await client.get("/api/v1/units/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_units(client: AsyncClient):
    """Test getting all units"""
    response = await client.get("/api/v1/units/")  
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_update_unit(client: AsyncClient, sample_unit):
    """Test updating a unit"""
    response = await client.put(
        f"/api/v1/units/{sample_unit['id']}",
        json={
            "name": "Updated Unit Name",
            "location": "Updated Location"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Unit Name"
    assert data["location"] == "Updated Location"


@pytest.mark.asyncio
async def test_delete_unit(client: AsyncClient):
    """Test deleting a unit"""
    # Create a unit first
    create_response = await client.post(
        "/api/v1/units/",
        json={
            "name": "Unit to Delete",
            "location": "Temporary Location"
        }
    )
    unit_id = create_response.json()["id"]
    
    # Delete it
    delete_response = await client.delete(f"/api/v1/units/{unit_id}")  
    assert delete_response.status_code == 200
    
    # Verify it's deleted
    get_response = await client.get(f"/api/v1/units/{unit_id}")  
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_unit_statistics(client: AsyncClient, sample_unit, sample_sensor):
    """Test getting unit statistics"""
    response = await client.get(f"/api/v1/units/{sample_unit['id']}/statistics")  
    assert response.status_code == 200
    data = response.json()
    assert "unit_id" in data
    assert "total_sensors" in data
    assert "active_sensors" in data
    assert data["unit_id"] == sample_unit["id"]