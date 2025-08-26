import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from src.db.session import init_db, engine
from src.api.v1 import main_router
from src.core.logging import setup_logging

setup_logging()
logger = logging.getLogger("src")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    await init_db(app)
    yield
    logger.info("Shutting down application")
    if hasattr(app.state, "db_pool"):
        await app.state.db_pool.close()
    await engine.dispose()


app = FastAPI(
    title="Task Manager API",
    version="0.1.0",
    description="API for task management with CRUD operations",
    lifespan=lifespan,
)

app.include_router(main_router, prefix="/api/v1/tasks", tags=["tasks"])


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def healthcheck():
    return {"status": "healthy"}
