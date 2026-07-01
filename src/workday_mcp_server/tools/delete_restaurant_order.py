from workday_mcp_server.workday_client import WorkdayClient

client = WorkdayClient()


async def delete_restaurant_order(id: str):
    if not id or id in ["$id", "undefined"]:
        return {
            "error": (
                "Missing required parameter 'id'. "
                "Use get_restaurant_orders_wql_tool first to find the restaurant order id."
            )
        }

    return await client.delete(
        f"/restaurantOrders/{id}"
    )