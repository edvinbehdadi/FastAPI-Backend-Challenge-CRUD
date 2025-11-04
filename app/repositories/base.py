from abc import ABC, abstractmethod
from typing import Optional, List, Any, Dict
import asyncpg
from app.database import DatabasePool


class BaseRepository(ABC):
    """Base repository class with common database operations"""
    
    def __init__(self):
        self.pool = DatabasePool.get_pool()
    
    async def execute(self, query: str, *args) -> str:
        """Execute a query that modifies data (INSERT, UPDATE, DELETE)"""
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)
    
    async def fetch_one(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Fetch a single row"""
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)
    
    async def fetch_all(self, query: str, *args) -> List[asyncpg.Record]:
        """Fetch all rows"""
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)
    
    async def fetch_val(self, query: str, *args) -> Any:
        """Fetch a single value"""
        async with self.pool.acquire() as connection:
            return await connection.fetchval(query, *args)
    
    @staticmethod
    def record_to_dict(record: Optional[asyncpg.Record]) -> Optional[Dict]:
        """Convert asyncpg.Record to dictionary"""
        if record is None:
            return None
        return dict(record)
    
    @staticmethod
    def records_to_list(records: List[asyncpg.Record]) -> List[Dict]:
        """Convert list of asyncpg.Record to list of dictionaries"""
        return [dict(record) for record in records]
