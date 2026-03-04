from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)


@app.get("/health")
async def health() -> dict:
    # health básico + ping a DB
    try:
        async for db in get_db():
            assert isinstance(db, AsyncSession)
            await db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "degraded", "db": "error", "detail": str(e)}
