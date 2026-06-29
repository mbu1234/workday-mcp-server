from workday_mcp_server.workday_client import WorkdayClient

client = WorkdayClient()

QUERY = (
    "SELECT orderMonth, orderYear, restaurant{name, type}, "
    "orderItems{itemName,quantity} "
    "FROM wendMealOrderDoNotDelete_zrclrm_restaurantOrders"
)


async def get_restaurant_orders_wql():
    return await client.get(
        "/restaurantOrders",
        params={"query": QUERY},
    )