from typing import Any

from ..workday_client import WorkdayClient

client = WorkdayClient()


async def list_restaurant_orders() -> Any:
    """
    Get restaurant orders from the Workday REST API.
    """
    return await client.get("/restaurantOrders")