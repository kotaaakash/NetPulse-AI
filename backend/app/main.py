from fastapi import FastAPI

from app.core.config import settings
from app.api.configuration import router as configuration_router
from app.api.diff import router as diff_router
from app.api.change_request import router as change_request_router
from app.api import audit_log

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-Powered Network Change Risk & Operations Platform",
)

app.include_router(configuration_router)
app.include_router(diff_router)
app.include_router(change_request_router)
app.include_router(audit_log.router)


@app.get("/")
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": settings.DATABASE_NAME,
        "status": "Running 🚀",
    }