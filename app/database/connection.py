import asyncpg
from typing import Optional
from app.config import settings


class DatabasePool:
    _pool: Optional[asyncpg.Pool] = None
    
    @classmethod
    async def create_pool(cls):
        """Create database connection pool"""
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                host=settings.database_host,
                port=settings.database_port,
                database=settings.database_name,
                user=settings.database_user,
                password=settings.database_password,
                min_size=5,
                max_size=20,
            )
        return cls._pool
    
    @classmethod
    async def close_pool(cls):
        """Close database connection pool"""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
    
    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        """Get the current pool instance"""
        if cls._pool is None:
            raise RuntimeError("Database pool not initialized. Call create_pool() first.")
        return cls._pool
