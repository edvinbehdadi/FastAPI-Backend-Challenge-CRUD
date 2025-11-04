from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.database import DatabasePool
from app.routers import units, sensors, sensor_data
from app.exception_handlers import register_exception_handlers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting up application...")
    try:
        await DatabasePool.create_pool()
        logger.info("Database pool initialized successfully")
    except Exception as e:
        logger.critical(f"Failed to initialize database pool: {str(e)}")
        raise
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("Shutting down application...")
    try:
        await DatabasePool.close_pool()
        logger.info("Database pool closed successfully")
    except Exception as e:
        logger.error(f"Error closing database pool: {str(e)}")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Sensor Management API",
    description="API for managing units, sensors, and sensor data",
    version="1.0.0",
    lifespan=lifespan
)

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(units.router, prefix="/api/v1")
app.include_router(sensors.router, prefix="/api/v1")
app.include_router(sensor_data.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sensor Management API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        pool = DatabasePool.get_pool()
        # Try to get a connection to verify pool is working
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }