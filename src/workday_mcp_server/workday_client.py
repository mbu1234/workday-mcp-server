import os
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

from .workday_auth import get_bearer_token

load_dotenv()


class WorkdayApiError(Exception):
    """Raised when a Workday REST API call fails."""


class WorkdayClient:
    def __init__(self) -> None:
        self.api_base = os.getenv("WORKDAY_API_BASE", "https://api.workday.com").rstrip("/")

    async def request(
        self,
        method: str,
        path: str,
        json_body: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        token = await get_bearer_token()

        url = f"{self.api_base}/{path.lstrip('/')}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=json_body,
                params=params,
            )

        if response.status_code >= 400:
            raise WorkdayApiError(
                f"Workday API error. "
                f"Method: {method}. "
                f"URL: {url}. "
                f"Status: {response.status_code}. "
                f"Response: {response.text}"
            )

        if not response.text:
            return {"status": "success"}

        return response.json()

    async def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        return await self.request(
            method="GET",
            path=path,
            params=params,
        )

    async def post(
        self,
        path: str,
        json_body: dict[str, Any],
    ) -> Any:
        return await self.request(
            method="POST",
            path=path,
            json_body=json_body,
        )

    async def put(
        self,
        path: str,
        json_body: dict[str, Any],
    ) -> Any:
        return await self.request(
            method="PUT",
            path=path,
            json_body=json_body,
        )

    async def delete(
        self,
        path: str,
    ) -> Any:
        return await self.request(
            method="DELETE",
            path=path,
        )