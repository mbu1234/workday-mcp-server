from typing import Any

from ..workday_client import WorkdayClient

client = WorkdayClient()


async def list_restaurants() -> Any:
    """
    Get the list of restaurants from the Workday restaurants REST API.
    """

    return await client.get(
        "/apps/wendMealOrderDoNotDelete_zrclrm/v1/restaurants"
    )