import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.routers import notifications
from app.services.email_engine import EmailService

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Notifications Microservice...")
    EmailService.load_locales()
    yield
    logger.info("🛑 Shutting down Notifications Microservice...")


app = FastAPI(title="Notifications Microservice", lifespan=lifespan)

app.include_router(notifications.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104
