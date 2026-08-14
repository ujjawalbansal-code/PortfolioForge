# motor is an async driver for fastapi but we use beanie cause that gives async as well as in-built pydantic support

import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
 
from models import User, Project, Certificate, Portfolio, Info
 
MONGO_URL = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "aiPortfolioBuilder")
 
client=None
 
 
async def init_db():
    """
    Called  once from app.py's lifespan startup.
    Creates the motor client and registers all Document models with beanie.
    """
    global client
    client = AsyncIOMotorClient(MONGO_URL)
 
    await init_beanie(
        database=client[DATABASE_NAME],
        document_models=[
            User,
            Info,
            Project,
            Certificate,
            Section,
            Card,
        ],
    )
 
 
async def close_db():
    """Called from app.py's lifespan shutdown to close the connection cleanly."""
    global client
    if client is not None:
        client.close()
 
