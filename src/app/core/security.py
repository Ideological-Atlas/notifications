import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.security.utils import get_authorization_scheme_param

from app.core.config import settings

logger = logging.getLogger(__name__)

AUTH_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


async def api_key_auth(auth_value: str | None = Depends(AUTH_HEADER)) -> str:
    scheme, param = get_authorization_scheme_param(auth_value)

    if scheme.lower() != "bearer" or param != settings.API_KEY:
        logger.warning("Unauthorized access attempt: Invalid Key or Scheme.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return param
