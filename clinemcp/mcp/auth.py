"""Bearer token authentication (ported from TOBOR)."""

import logging
import os
import secrets
from typing import Annotated

from fastapi import HTTPException, Header

logger = logging.getLogger(__name__)

ALLOW_NO_AUTH_ENV = "CLINEMCP_ALLOW_NO_AUTH"


def get_auth_token() -> str:
    """Get auth token from environment."""
    token = os.environ.get("CLINEMCP_AUTH_TOKEN", "")
    if not token:
        # Fallback for development
        token = os.environ.get("DUGGERBOT_AUTH_TOKEN", "")
    return token


def auth_disabled_explicitly() -> bool:
    """True only when the operator explicitly opted out of auth."""
    return os.environ.get(ALLOW_NO_AUTH_ENV, "") == "1"


def log_auth_config() -> None:
    """Log a clear warning at startup if auth is not configured."""
    if get_auth_token():
        return
    if auth_disabled_explicitly():
        logger.warning(
            f"No CLINEMCP_AUTH_TOKEN configured and {ALLOW_NO_AUTH_ENV}=1 — "
            "ALL requests are allowed without authentication."
        )
    else:
        logger.warning(
            "No CLINEMCP_AUTH_TOKEN configured — all authenticated endpoints "
            f"will reject requests with 401. Set CLINEMCP_AUTH_TOKEN, or set "
            f"{ALLOW_NO_AUTH_ENV}=1 to explicitly disable auth (development only)."
        )


async def verify_token_dependency(
    authorization: Annotated[str | None, Header()] = None,
) -> bool:
    """FastAPI dependency to verify Bearer token.

    Returns True if token valid.
    Fails closed: if no token is configured, raises 401 unless
    CLINEMCP_ALLOW_NO_AUTH=1 is set.
    Raises HTTPException 401 if token invalid.
    """
    expected_token = get_auth_token()
    if not expected_token:
        if auth_disabled_explicitly():
            return True
        raise HTTPException(status_code=401, detail="Server auth token not configured")

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")

    provided_token = authorization[7:].strip()  # Remove "Bearer " prefix

    if not secrets.compare_digest(provided_token.encode(), expected_token.encode()):
        raise HTTPException(status_code=401, detail="Invalid token")

    return True
