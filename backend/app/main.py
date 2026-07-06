from fastapi import FastAPI

from app.core.config import settings
from app.api.configuration import router as configuration_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-Powered Network Change Risk & Operations Platform",
)

app.include_router(configuration_router)


@app.get("/")
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": settings.DATABASE_NAME,
        "status": "Running 🚀",
    }