# 🏛️ Architecture Documentation

## Overview

This project follows a **layered architecture** with clear separation of concerns, implementing the **Repository Pattern** without using an ORM.

## Architectural Layers

```
┌─────────────────────────────────────────┐
│         API Layer (FastAPI)             │  ← HTTP Request/Response
├─────────────────────────────────────────┤
│         Service Layer                   │  ← Business Logic
├─────────────────────────────────────────┤
│      Repository Layer                   │  ← Data Access (Raw SQL)
├─────────────────────────────────────────┤
│         Database (PostgreSQL)           │  ← Data Storage
└─────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. API Layer (`app/api/`)

**Purpose**: Handle HTTP requests and responses

**Responsibilities**:
- Route definition and HTTP method mapping
- Request validation (via Pydantic)
- Response formatting
- HTTP status codes
- Query parameters handling

**Example**:
```python
@router.post("/", response_model=Unit, status_code=status.HTTP_201_CREATED)
async def create_unit(unit: UnitCreate):
    service = UnitService()
    return await service.create_unit(unit)
```

**Key Points**:
- Thin layer - minimal logic
- No direct database access
- Delegates to Service layer
- Returns Pydantic models

### 2. Service Layer (`app/services/`)

**Purpose**: Business logic and orchestration

**Responsibilities**:
- Business rule validation
- Error handling and exception mapping
- Orchestrating multiple repository calls
- Transaction coordination (if needed)
- Converting between repository data and domain models

**Example**:
```python
class UnitService:
    def __init__(self):
        self.repository = UnitRepository()
    
    async def create_unit(self, unit: UnitCreate) -> Unit:
        unit_data = await self.repository.create(unit)
        return Unit(**unit_data)
```

**Key Points**:
- Contains business logic
- Raises HTTP exceptions
- No SQL queries here
- Converts dict to Pydantic models

### 3. Repository Layer (`app/repositories/`)

**Purpose**: Data access and persistence

**Responsibilities**:
- Execute SQL queries
- Connection management
- Query result transformation
- CRUD operations
- Custom queries

**Example**:
```python
class UnitRepository(BaseRepository):
    async def create(self, unit: UnitCreate) -> Dict:
        query = """
            INSERT INTO units (name, location, description)
            VALUES ($1, $2, $3)
            RETURNING id, name, location, description, created_at
        """
        record = await self.fetch_one(query, unit.name, unit.location, unit.description)
        return self.record_to_dict(record)
```

**Key Points**:
- Raw SQL queries (no ORM)
- Uses asyncpg
- Returns dictionaries
- No business logic

### 4. Model Layer (`app/models/`)

**Purpose**: Data validation and serialization

**Responsibilities**:
- Define data structures
- Input validation
- Response serialization
- Type checking

**Types of Models**:
- **Base**: Common fields
- **Create**: Fields required for creation
- **Update**: Optional fields for updates
- **Response**: Complete model with all fields

## Repository Pattern Implementation

### Base Repository

Provides common database operations:

```python
class BaseRepository(ABC):
    def __init__(self):
        self.pool = DatabasePool.get_pool()
    
    async def execute(self, query: str, *args) -> str:
        """Execute INSERT, UPDATE, DELETE"""
        
    async def fetch_one(self, query: str, *args) -> Optional[Record]:
        """Fetch single row"""
        
    async def fetch_all(self, query: str, *args) -> List[Record]:
        """Fetch multiple rows"""
```

### Concrete Repositories

Each entity has its own repository extending `BaseRepository`:

- `UnitRepository`
- `SensorRepository`
- `SensorDataRepository`

## Database Connection Management

### Connection Pool

Uses asyncpg connection pool for efficient connection management:

```python
class DatabasePool:
    _pool: Optional[asyncpg.Pool] = None
    
    @classmethod
    async def create_pool(cls):
        cls._pool = await asyncpg.create_pool(...)
    
    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        return cls._pool
```

**Benefits**:
- Connection reuse
- Automatic connection recovery
- Configurable pool size
- Better performance

## Data Flow

### Create Operation Example

```
User Request (POST /api/units/)
    ↓
API Layer (units.py)
    - Validates request body
    - Creates UnitService instance
    ↓
Service Layer (unit_service.py)
    - Calls repository.create()
    - Converts dict to Unit model
    ↓
Repository Layer (unit_repository.py)
    - Executes SQL INSERT
    - Returns dict with created data
    ↓
Database (PostgreSQL)
    - Stores data
    - Returns created record
    ↓
Response flows back up (Unit model → JSON)
```

### Read with Relationships Example

```
GET /api/units/1/statistics
    ↓
API Layer
    ↓
Service Layer
    - Validates unit exists
    - Calls repository.get_statistics()
    ↓
Repository Layer
    - Executes SQL JOIN query
    - Aggregates data
    - Returns dict
    ↓
Service converts to UnitStatistics model
    ↓
API returns JSON
```

## SOLID Principles Application

### Single Responsibility Principle (SRP)

Each class has one reason to change:
- **API**: HTTP handling
- **Service**: Business logic
- **Repository**: Data access

### Open/Closed Principle (OCP)

- Base repository open for extension
- Concrete repositories extend without modifying base
- New features added without changing existing code

### Liskov Substitution Principle (LSP)

- All repositories implement same interface
- Can swap repository implementations
- Follows base repository contract

### Interface Segregation Principle (ISP)

- Small, focused interfaces
- Repositories have specific methods
- No unnecessary dependencies

### Dependency Inversion Principle (DIP)

- High-level (Service) doesn't depend on low-level (Repository details)
- Both depend on abstractions
- Dependency injection used

## Database Design

### Entities

1. **Units**: Physical locations/organizational units
2. **Sensors**: IoT devices attached to units
3. **SensorData**: Readings from sensors

### Relationships

```
Units (1) ─────< (N) Sensors
                      │
                      │
                      ↓
              SensorData (N)
```

### Foreign Keys

- `sensors.unit_id` → `units.id` (CASCADE DELETE)
- `sensor_data.sensor_id` → `sensors.id` (CASCADE DELETE)

### Indexes

Strategic indexes for performance:
- Primary keys (automatic)
- Foreign keys
- Timestamp fields
- Commonly filtered fields

## Migration Strategy

Using Alembic for database migrations:

1. **Version Control**: Each migration has unique version
2. **Up/Down**: Support rollback
3. **SQL-Based**: Raw SQL for control
4. **Sequential**: Migrations applied in order

## Error Handling

### Layered Error Handling

```
Repository Layer
    - asyncpg errors
    - Connection errors
    ↓
Service Layer
    - Business rule violations
    - Not found errors (404)
    - Validation errors (400)
    - Convert to HTTPException
    ↓
API Layer
    - FastAPI automatic error responses
    - Consistent error format
```

## Testing Strategy

### Unit Tests Structure

```
tests/
    ├── conftest.py          # Fixtures
    ├── test_units.py        # Unit API tests
    ├── test_sensors.py      # Sensor API tests
    └── test_sensor_data.py  # SensorData API tests
```

### Test Coverage

- API endpoint tests
- CRUD operations
- Business logic validation
- Error cases
- Relationships

## Performance Considerations

### Connection Pooling

- Min connections: 5
- Max connections: 20
- Automatic recovery

### Query Optimization

- Proper indexing
- Efficient JOINs
- Parameterized queries (prevent SQL injection)

### Pagination

- Limit maximum results (100)
- Offset-based pagination
- Prevent large data transfers

## Security Considerations

### SQL Injection Prevention

Using parameterized queries:
```python
query = "SELECT * FROM units WHERE id = $1"
await connection.fetchrow(query, unit_id)
```

### Input Validation

- Pydantic models validate all inputs
- Type checking
- Length constraints
- Enum validation

## Scalability

### Horizontal Scaling

- Stateless API design
- Connection pool per instance
- Database connection limit management

### Vertical Scaling

- Async operations (asyncio)
- Connection pooling
- Efficient queries

## Future Enhancements

1. **Caching**: Redis for frequently accessed data
2. **Authentication**: JWT tokens
3. **Authorization**: Role-based access control
4. **Pagination**: Cursor-based pagination
5. **Rate Limiting**: API usage limits
6. **Monitoring**: Prometheus metrics
7. **Logging**: Structured logging
8. **API Versioning**: Support multiple versions

## Conclusion

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Testability
- ✅ Maintainability
- ✅ Scalability
- ✅ SOLID compliance
- ✅ No ORM dependency
- ✅ Full SQL control
