import logging

from fastapi import Header, HTTPException

from app.core.config import settings

logger = logging.getLogger(__name__)


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        logger.warning("Unauthorized access attempt: Invalid API Key provided.")
        raise HTTPException(
            status_code=401, detail="Invalid Authentication Credentials"
        )
    return x_api_key
