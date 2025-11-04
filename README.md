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
│   ├── api/                          # API endpoints (routes)
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
   - **Alternative docs (ReDoc)**: http://localhost:8000/redoc
   - **OpenAPI Schema**: http://localhost:8000/openapi.json

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

## 📊 Database Schema

### Units Table
Physical locations or organizational units where sensors are deployed.

```sql
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(500) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose**: Represent facilities like factories, warehouses, or buildings.

### Sensors Table
IoT sensors attached to units for data collection.

```sql
CREATE TYPE sensor_type_enum AS ENUM (
    'temperature', 'humidity', 'pressure', 
    'motion', 'light', 'sound'
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
```

**Purpose**: Track individual sensors and their operational status.

### Sensor Data Table
Data readings collected from sensors.

```sql
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

2. **ReDoc** (Alternative): http://localhost:8000/redoc
   - Clean, readable documentation
   - Better for reading and understanding API structure
   - Detailed descriptions and examples
   - Mobile-friendly interface

3. **OpenAPI JSON**: http://localhost:8000/openapi.json
   - Raw OpenAPI specification
   - Import into Postman, Insomnia, or other tools
   - Generate client SDKs in any language

### Documentation Features:

- ✅ Comprehensive endpoint descriptions
- ✅ Request/response schemas with examples
- ✅ HTTP status codes documentation (200, 201, 404, 422, 500)
- ✅ Parameter descriptions and validation rules
- ✅ Model schemas with field descriptions
- ✅ Enum values and their meanings
- ✅ Interactive testing capability
- ✅ Error response examples

### Using Swagger UI:

1. Navigate to http://localhost:8000/docs
2. Browse available endpoints organized by tags (units, sensors, sensor-data)
3. Click on any endpoint to expand details
4. Click "Try it out" to test the endpoint
5. Fill in parameters and request body (examples provided)
6. Click "Execute" to send the request
7. View the response with status code and data

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

### Reinitializing Sample Data:

```bash
# Stop and remove containers including volumes
docker-compose down -v

# Rebuild and start (will reinitialize data)
docker-compose up --build
```

### Manual Sample Data Initialization:

```bash
# With Docker
docker-compose exec api python scripts/init_sample_data.py

# Locally
python scripts/init_sample_data.py
```

**Note:** The initialization script is idempotent - it checks if data exists and won't duplicate entries.

## 📝 API Usage Examples

### Create a Unit
```bash
curl -X POST "http://localhost:8000/api/units/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Factory A",
    "location": "Building 1, Floor 2",
    "description": "Main production unit"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Factory A",
  "location": "Building 1, Floor 2",
  "description": "Main production unit",
  "created_at": "2025-01-15T10:30:00Z"
}
```

### Create a Sensor
```bash
curl -X POST "http://localhost:8000/api/sensors/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Temperature Sensor 1",
    "sensor_type": "temperature",
    "unit_id": 1,
    "status": "active",
    "description": "Monitors room temperature"
  }'
```

**Available Sensor Types:**
- `temperature` - Temperature sensors
- `humidity` - Humidity sensors
- `pressure` - Pressure sensors
- `motion` - Motion detectors
- `light` - Light sensors
- `sound` - Sound level meters

### Create Sensor Data
```bash
curl -X POST "http://localhost:8000/api/sensor-data/" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": 1,
    "value": 23.5,
    "unit": "celsius",
    "status": "pending"
  }'
```

### Validate Sensor Data
```bash
curl -X PUT "http://localhost:8000/api/sensor-data/1/validate" \
  -H "Content-Type: application/json"
```

### Archive Sensor Data
```bash
curl -X PUT "http://localhost:8000/api/sensor-data/1/archive" \
  -H "Content-Type: application/json"
```

### Get Unit Statistics
```bash
curl "http://localhost:8000/api/units/1/statistics"
```

**Response:**
```json
{
  "unit_id": 1,
  "unit_name": "Factory A",
  "total_sensors": 5,
  "active_sensors": 4,
  "inactive_sensors": 1,
  "total_data_points": 1250,
  "latest_data_timestamp": "2025-01-15T14:30:00Z"
}
```

### Get Sensors with Filtering
```bash
# Get all sensors for a specific unit
curl "http://localhost:8000/api/sensors/?unit_id=1"

# Get paginated results
curl "http://localhost:8000/api/sensors/?skip=0&limit=10"
```

### Get Sensor Data with Filtering
```bash
# Get all data for a specific sensor
curl "http://localhost:8000/api/sensor-data/?sensor_id=1"

# Get only validated data
curl "http://localhost:8000/api/sensor-data/?status=validated"

# Get data with sensor and unit details
curl "http://localhost:8000/api/sensor-data/?with_details=true"
```

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

### Test Output Example:
```
tests/test_units.py::test_create_unit PASSED           [ 14%]
tests/test_units.py::test_get_unit PASSED              [ 28%]
tests/test_units.py::test_update_unit PASSED           [ 42%]
tests/test_sensors.py::test_create_sensor PASSED       [ 57%]
tests/test_sensor_data.py::test_validate_data PASSED   [ 71%]
...
======================== 38 passed in 2.45s =========================
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

### SOLID Principles

**Single Responsibility Principle (SRP)**:
- Each class has one reason to change
- Repositories: data access only
- Services: business logic only
- Routes: HTTP handling only

**Open/Closed Principle (OCP)**:
- Base repository provides common functionality
- Extended without modifying base

**Liskov Substitution Principle (LSP)**:
- All repositories follow the same contract
- Interchangeable implementations

**Interface Segregation Principle (ISP)**:
- Focused interfaces
- No unnecessary methods

**Dependency Inversion Principle (DIP)**:
- High-level modules don't depend on low-level modules
- Both depend on abstractions

### Exception Handling

Custom exceptions for different error scenarios:

```python
NotFoundException       # 404 - Resource not found
BadRequestException     # 400 - Invalid request
ValidationException     # 422 - Validation error
ConflictException      # 409 - Conflict (duplicate, etc.)
DatabaseException      # 500 - Database error
InternalServerException # 500 - Unexpected error
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

### Docker Environment

For Docker, the database host is `db` (service name):

```env
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=iot_sensors
DATABASE_USER=iot_user
DATABASE_PASSWORD=1245
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

### Development Dependencies:
- **Alembic**: Database migrations
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **httpx**: HTTP client for testing

### Full Requirements:
See `requirements.txt` for complete list with versions.

## 🐳 Docker Configuration

### Services:

**Database (PostgreSQL 15)**:
- Image: `postgres:15-alpine`
- Port: 5432
- Persistent volume for data
- Health checks enabled

**API (FastAPI)**:
- Built from `Dockerfile`
- Port: 8000
- Auto-reload enabled
- Depends on database health

### Docker Commands:

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v

# Execute command in container
docker-compose exec api bash

# Run tests
docker-compose exec api pytest
```

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

**Use Cases**:
- Dashboard visualization
- System health monitoring
- Capacity planning
- Performance analysis

## 🔒 Production Considerations

### Security:
- [ ] Add authentication (JWT, OAuth2)
- [ ] Implement authorization (RBAC)
- [ ] Use HTTPS/TLS
- [ ] Add rate limiting
- [ ] Sanitize inputs
- [ ] Use secrets management (AWS Secrets Manager, Vault)
- [ ] Enable CORS properly
- [ ] Add security headers

### Performance:
- [ ] Add Redis caching
- [ ] Optimize database indexes
- [ ] Implement connection pooling limits
- [ ] Add request/response compression
- [ ] Use CDN for static assets
- [ ] Implement pagination everywhere
- [ ] Add query optimization
- [ ] Use database read replicas

### Monitoring:
- [ ] Add structured logging (JSON)
- [ ] Implement health checks (`/health`, `/ready`)
- [ ] Add metrics collection (Prometheus)
- [ ] Set up alerting (PagerDuty, Slack)
- [ ] Add APM (Application Performance Monitoring)
- [ ] Track error rates
- [ ] Monitor response times
- [ ] Log slow queries

### Reliability:
- [ ] Add retry logic with exponential backoff
- [ ] Implement circuit breakers
- [ ] Add request timeouts
- [ ] Set up automated database backups
- [ ] Implement graceful shutdown
- [ ] Add health check endpoints
- [ ] Use blue-green deployments
- [ ] Set up disaster recovery

### DevOps:
- [ ] Set up CI/CD pipeline
- [ ] Automate testing
- [ ] Container orchestration (Kubernetes)
- [ ] Infrastructure as Code (Terraform)
- [ ] Automated scaling
- [ ] Log aggregation (ELK, Splunk)
- [ ] Secret rotation
- [ ] Automated rollbacks

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

#### 4. Docker Build Issues

**Error**: `failed to compute cache key`

**Solution**:
```bash
# Clear Docker cache
docker-compose down
docker system prune -a
docker-compose build --no-cache
```

#### 5. Database Connection Issues

**Error**: `could not connect to server`

**Solution**:
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Test connection
psql -U iot_user -d iot_sensors -h localhost

# Check Docker network
docker network ls
docker network inspect <network_name>
```

#### 6. Migration Issues

**Error**: `target database is not up to date`

**Solution**:
```bash
# Check current version
alembic current

# View history
alembic history

# Stamp current version
alembic stamp head

# Or downgrade and upgrade
alembic downgrade base
alembic upgrade head
```

### Debug Mode:

Enable detailed logging:

```python
# In app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help:

1. Check application logs:
```bash
docker-compose logs api
```

2. Check database logs:
```bash
docker-compose logs db
```

3. Access container shell:
```bash
docker-compose exec api bash
```

## 📄 License

This project is developed as a technical assessment for recruitment purposes.

## 👨‍💻 Author

**Developed by:** Edvin ‌Behdadi

**Project Type:** FastAPI Backend Challenge - IoT Sensors Management System

**Technologies Used:**
- FastAPI
- PostgreSQL
- asyncpg
- Alembic
- Docker
- pytest

---



**Note**: This is a demonstration project showcasing clean architecture, best practices, and production-ready code structure. All sample data is fictional and for demonstration purposes only.