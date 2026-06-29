import os
import time
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class WorkdayAuthError(Exception):
    """Raised when Workday OAuth authentication fails."""


_cached_token: Optional[str] = None
_token_expires_at: float = 0


async def get_bearer_token() -> str:
    """
    Gets a Workday bearer token using the refresh token flow.

    The token is cached in memory until shortly before it expires.
    """

    global _cached_token, _token_expires_at

    now = time.time()

    if _cached_token and now < _token_expires_at:
        return _cached_token

    auth_url = os.getenv("WORKDAY_AUTH_URL")
    client_id = os.getenv("WORKDAY_CLIENT_ID")
    refresh_token = os.getenv("WORKDAY_REFRESH_TOKEN")
    authorization_id = os.getenv("WORKDAY_AUTHORIZATION_ID")

    if not auth_url:
        raise WorkdayAuthError("Missing WORKDAY_AUTH_URL environment variable.")

    if not client_id:
        raise WorkdayAuthError("Missing WORKDAY_CLIENT_ID environment variable.")

    if not refresh_token:
        raise WorkdayAuthError("Missing WORKDAY_REFRESH_TOKEN environment variable.")

    if not authorization_id:
        raise WorkdayAuthError("Missing WORKDAY_AUTHORIZATION_ID environment variable.")

    form_data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": authorization_id,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            auth_url,
            data=form_data,
            headers=headers,
        )

    if response.status_code >= 400:
        raise WorkdayAuthError(
            f"Authorization fetch failed. "
            f"Status {response.status_code}: {response.text}"
        )

    auth_data = response.json()

    access_token = auth_data.get("access_token")

    if not access_token:
        raise WorkdayAuthError("Access token was not found in the authentication response.")

    expires_in = auth_data.get("expires_in", 3600)

    _cached_token = access_token
    _token_expires_at = now + int(expires_in) - 60

    return access_token