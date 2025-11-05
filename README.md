# 🐍 FastAPI IoT Sensors API

A production-ready REST API for managing IoT sensors and their data, built with FastAPI and PostgreSQL without ORM, using the Repository Pattern.

## 📋 Features

- ✅ Complete CRUD operations for Units, Sensors, and Sensor Data
- ✅ Repository Pattern (without ORM)
- ✅ Raw SQL queries with asyncpg
- ✅ Database migrations with Alembic
- ✅ Comprehensive unit tests with pytest
- ✅ Docker containerization with sample data initialization
- ✅ Clean architecture (layers: API → Service → Repository)
- ✅ SOLID principles implementation
- ✅ Type hints and Pydantic validation
- ✅ Statistics and aggregation endpoints
- ✅ Custom exception handling
- ✅ Comprehensive logging
- ✅ OpenAPI/Swagger documentation

## 🏗️ Project Structure

```
FastAPI-Backend-Challenge-CRUD/
├── app/
│   ├── routers/                          # API endpoints (routes)
│   │   ├── __init__.py
│   │   ├── units.py                  # Unit endpoints
│   │   ├── sensors.py                # Sensor endpoints
│   │   └── sensor_data.py            # Sensor data endpoints
│   ├── models/                       # Pydantic models
│   │   ├── __init__.py
│   │   ├── unit.py                   # Unit models
│   │   ├── sensor.py                 # Sensor models (with enums)
│   │   └── sensor_data.py            # Sensor data models
│   ├── repositories/                 # Data access layer (Repository Pattern)
│   │   ├── __init__.py
│   │   ├── base.py                   # Base repository with common methods
│   │   ├── unit_repository.py        # Unit data access
│   │   ├── sensor_repository.py      # Sensor data access
│   │   └── sensor_data_repository.py # Sensor data access
│   ├── services/                     # Business logic layer
│   │   ├── __init__.py
│   │   ├── unit_service.py           # Unit business logic
│   │   ├── sensor_service.py         # Sensor business logic
│   │   └── sensor_data_service.py    # Sensor data business logic
│   ├── schemas/                      # API schemas and examples
│   │   ├── __init__.py
│   │   └── api_examples.py           # OpenAPI examples and descriptions
│   ├── database/                     # Database connection
│   │   ├── __init__.py
│   │   └── connection.py             # Database pool management
│   ├── exceptions/                   # Custom exceptions
│   │   └── __init__.py
│   ├── config.py                     # Application configuration
│   └── main.py                       # FastAPI application setup
├── alembic/                          # Database migrations
│   ├── versions/                     # Migration files
│   │   └── xxxx_initial_migration.py
│   ├── env.py                        # Alembic environment
│   └── script.py.mako                # Migration template
├── scripts/                          # Utility scripts
│   └── init_sample_data.py           # Sample data initialization
├── tests/                            # Unit tests
│   ├── __init__.py
│   ├── conftest.py                   # Test fixtures
│   ├── test_units.py                 # Unit endpoint tests
│   ├── test_sensors.py               # Sensor endpoint tests
│   └── test_sensor_data.py           # Sensor data endpoint tests
├── .env                              # Environment variables (not in git)
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── alembic.ini                       # Alembic configuration
├── docker-compose.yml                # Docker Compose configuration
├── Dockerfile                        # Docker image definition
├── pytest.ini                        # Pytest configuration
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Running with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/edvinbehdadi/FastAPI-Backend-Challenge-CRUD.git
cd FastAPI-Backend-Challenge-CRUD
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env if needed (default values work with Docker)
```

3. Start the application:
```bash
docker-compose up --build
```

4. The API will be available at:
   - **API**: http://localhost:8000
   - **Interactive docs (Swagger)**: http://localhost:8000/docs

**Note:** On first startup, the application will automatically:
- Create database tables via Alembic migrations
- Initialize sample data (units, sensors, and sensor readings)

To reset and reinitialize data:
```bash
docker-compose down -v
docker-compose up --build
```

### Running Locally (without Docker)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install and setup PostgreSQL:
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE iot_sensors;
CREATE USER iot_user WITH PASSWORD 'your_password';
ALTER DATABASE iot_sensors OWNER TO iot_user;
ALTER SCHEMA public OWNER TO iot_user;
GRANT ALL PRIVILEGES ON DATABASE iot_sensors TO iot_user;
\q
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials:
# DATABASE_HOST=localhost
# DATABASE_USER=iot_user
# DATABASE_PASSWORD=your_password
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Initialize sample data (optional):
```bash
python scripts/init_sample_data.py
```

7. Start the application:
```bash
uvicorn app.main:app --reload
```

**Purpose**: Store time-series data from sensors with validation workflow.

## 🔌 API Endpoints

### Units Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/units/` | Create a new unit |
| GET | `/api/units/` | Get all units (paginated) |
| GET | `/api/units/{id}` | Get unit by ID |
| PUT | `/api/units/{id}` | Update unit |
| DELETE | `/api/units/{id}` | Delete unit (cascades to sensors and data) |
| GET | `/api/units/{id}/statistics` | Get unit statistics |

### Sensors Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sensors/` | Create a new sensor |
| GET | `/api/sensors/` | Get all sensors (filter by unit_id) |
| GET | `/api/sensors/{id}` | Get sensor by ID |
| PUT | `/api/sensors/{id}` | Update sensor |
| DELETE | `/api/sensors/{id}` | Delete sensor (cascades to data) |

### Sensor Data Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sensor-data/` | Create new sensor data |
| GET | `/api/sensor-data/` | Get all sensor data (filter by sensor_id, status) |
| GET | `/api/sensor-data/{id}` | Get sensor data by ID |
| PUT | `/api/sensor-data/{id}` | Update sensor data |
| PUT | `/api/sensor-data/{id}/validate` | Mark data as validated |
| PUT | `/api/sensor-data/{id}/archive` | Mark data as archived |
| DELETE | `/api/sensor-data/{id}` | Delete sensor data |

## 📚 API Documentation (OpenAPI)

This API is fully documented using **OpenAPI 3.0** specification with comprehensive examples and descriptions.

### Accessing Documentation:

1. **Swagger UI** (Interactive): http://localhost:8000/docs
   - Try out API calls directly from the browser
   - See request/response examples for all endpoints
   - Test different scenarios with pre-filled examples
   - View all schemas and models with descriptions

### API Examples in Documentation:

Each endpoint includes pre-filled examples:
- **Units**: Factory locations, warehouses, office buildings
- **Sensors**: Temperature, humidity, pressure sensors
- **Sensor Data**: Real-time readings with different statuses

## 🎲 Sample Data

The application automatically initializes with realistic sample data on first startup.

### What's Included:

- **4 Units**: Different types of facilities
- **Multiple Sensors per Unit**: Various sensor types
- **Time-series Data**: Realistic sensor readings

### Sample Data Details:

**Units:**
- Factory A - Production Floor (Building 1, Floor 2)
- Warehouse B - Storage Area (Building 3, Ground Floor)
- Office Building C (Building 2, All Floors)
- Data Center (Building 4, Basement)

**Sensor Types:**
- **Temperature**: Monitoring ambient temperature (celsius)
- **Humidity**: Monitoring moisture levels (percentage)
- **Pressure**: Monitoring atmospheric pressure (pascal)
- **Motion**: Detecting movement (boolean/count)
- **Light**: Monitoring illumination (lux)
- **Sound**: Monitoring noise levels (decibels)

**Data Status Distribution:**
- Pending: Awaiting validation
- Validated: Confirmed as accurate
- Archived: Historical data

### Sample Data Workflow:

The sample data demonstrates a complete IoT monitoring scenario:

1. **Setup Phase**: Units and sensors are created
2. **Data Collection**: Sensors generate readings
3. **Validation**: Admin reviews and validates data
4. **Archival**: Old validated data is archived


## 🧪 Running Tests

The project includes comprehensive unit tests covering all endpoints and business logic.

### Test Coverage:

- ✅ Unit CRUD operations
- ✅ Sensor CRUD operations
- ✅ Sensor Data CRUD operations
- ✅ Validation workflow
- ✅ Archive workflow
- ✅ Error handling
- ✅ Edge cases

### Running Tests:

#### With Docker (Recommended):
```bash
# Run all tests
docker-compose exec api pytest

# Run with verbose output
docker-compose exec api pytest -v

# Run specific test file
docker-compose exec api pytest tests/test_units.py

# Run with coverage report
docker-compose exec api pytest --cov=app --cov-report=html
```

#### Locally:
```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_units.py

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```


## 🗄️ Database Migrations

The project uses Alembic for database schema management and versioning.

### Common Migration Commands:

```bash
# Create a new migration
alembic revision -m "description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Check current migration version
alembic current

# Reset to specific version
alembic downgrade <revision_id>
```

### Migration Workflow:

1. **Make Schema Changes**: Modify models or create new ones
2. **Generate Migration**: `alembic revision -m "add_new_field"`
3. **Edit Migration**: Review and modify the generated migration file
4. **Apply Migration**: `alembic upgrade head`
5. **Commit**: Commit the migration file to version control

### Migration Files Location:
```
alembic/versions/xxxx_migration_name.py
```

## 🎯 Architecture & Design Patterns

### Layered Architecture

```
┌─────────────────────────────────┐
│   API Layer (FastAPI Routes)   │  ← HTTP requests/responses
├─────────────────────────────────┤
│   Service Layer                 │  ← Business logic
├─────────────────────────────────┤
│   Repository Layer              │  ← Data access
├─────────────────────────────────┤
│   Database (PostgreSQL)         │  ← Data storage
└─────────────────────────────────┘
```

### Repository Pattern

**Purpose**: Abstract data access logic from business logic

**Benefits**:
- Separation of concerns
- Easier testing (can mock repositories)
- Centralized data access
- No ORM dependency

**Implementation**:
```python
class BaseRepository:
    """Base repository with common CRUD operations"""
    async def fetch_one(query, *args)
    async def fetch_all(query, *args)
    async def execute(query, *args)

class UnitRepository(BaseRepository):
    """Specific repository for Unit operations"""
    async def create(unit: UnitCreate)
    async def get_by_id(unit_id: int)
    async def update(unit_id: int, unit: UnitUpdate)
    async def delete(unit_id: int)
```

### Service Layer

**Purpose**: Contain business logic and orchestrate repository calls

**Responsibilities**:
- Validate business rules
- Handle exceptions
- Coordinate multiple repository operations
- Transform data between layers

**Example**:
```python
class UnitService:
    def __init__(self):
        self.repository = UnitRepository()
    
    async def create_unit(self, unit: UnitCreate) -> Unit:
        # Business logic here
        unit_data = await self.repository.create(unit)
        return Unit(**unit_data)
```


## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=iot_sensors
DATABASE_USER=iot_user
DATABASE_PASSWORD=your_password_here
```

### Configuration Files

- `.env` - Environment variables (not in git)
- `.env.example` - Template for environment variables
- `alembic.ini` - Alembic configuration
- `pytest.ini` - Pytest configuration
- `docker-compose.yml` - Docker services configuration

## 📦 Dependencies

### Core Dependencies:
- **FastAPI** (0.104+): Modern web framework
- **asyncpg**: Async PostgreSQL driver
- **Pydantic** (2.0+): Data validation
- **Uvicorn**: ASGI server
- **python-dotenv**: Environment variables

### Full Requirements:
See `requirements.txt` for complete list with versions.


## 📈 Statistics & Monitoring

### Unit Statistics Endpoint

`GET /api/units/{id}/statistics`

Provides comprehensive statistics for a unit:

```json
{
  "unit_id": 1,
  "unit_name": "Factory A",
  "total_sensors": 5,
  "active_sensors": 4,
  "inactive_sensors": 1,
  "maintenance_sensors": 0,
  "total_data_points": 1250,
  "latest_data_timestamp": "2025-01-15T14:30:00Z"
}
```


## 🐛 Troubleshooting

### Common Issues:

#### 1. PostgreSQL Permission Issues

**Error**: `permission denied for schema public`

**Solution**:
```bash
sudo -u postgres psql
\c iot_sensors
ALTER DATABASE iot_sensors OWNER TO iot_user;
ALTER SCHEMA public OWNER TO iot_user;
GRANT ALL ON SCHEMA public TO iot_user;
\q
```

#### 2. Port Already in Use

**Error**: `address already in use`

**Solution**:
```bash
# Find process using port 5432
sudo lsof -i :5432

# Kill the process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "5433:5432"
```

#### 3. psycopg2 Installation Issues

**Error**: `pg_config executable not found`

**Solution**:
```bash
# Install PostgreSQL development packages
sudo apt install libpq-dev python3-dev

# Or use binary version
pip install psycopg2-binary
```


## 👨‍💻 Author

**Developed by:** Edvin ‌Behdadi

**Project Type:** FastAPI Backend Challenge - IoT Sensors Management System

**Note**: This is a demonstration project showcasing clean architecture, best practices, and production-ready code structure. All sample data is fictional and for demonstration purposes only.