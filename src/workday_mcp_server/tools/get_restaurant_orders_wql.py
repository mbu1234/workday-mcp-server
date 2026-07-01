import httpx

from workday_mcp_server.workday_auth import get_bearer_token


WQL_QUERY = (
    "SELECT workdayID, orderMonth, orderYear, "
    "restaurant{name, type}, "
    "orderItems{itemName,quantity} "
    "FROM wendMealOrderDoNotDelete_zrclrm_restaurantOrders"
)


async def get_restaurant_orders_wql():
    token = await get_bearer_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            "https://api.us.wcp.workday.com/wql/v1/data",
            headers=headers,
            params={"query": WQL_QUERY},
        )

    response.raise_for_status()

    return response.json()