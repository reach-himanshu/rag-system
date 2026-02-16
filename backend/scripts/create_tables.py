import asyncio
import logging
import sys
from sqlalchemy.ext.asyncio import create_async_engine

# Add project root to path so we can import app modules
import os
sys.path.append(os.getcwd())

from app.config import settings
from app.db.models import Base
from app.db.session import engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_models():
    logger.info("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_models())
