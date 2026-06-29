from workday_mcp_server.workday_client import WorkdayClient

client = WorkdayClient()


async def patch_restaurant(
    id: str,
    name: str,
    type: str,
    active: bool,
):
    if not id or id in ["$id", "undefined"]:
        return (
            "TOOL_ERROR: The 'id' parameter is missing. "
            "You MUST call 'list_restaurants_tool' first, find the restaurant, "
            "extract the 'id' value, and then provide that specific 'id' to patch_restaurant_tool."
        )

    update_data = {
        "name": name,
        "type": type,
        "active": active,
    }

    return await client.request(
        method="PATCH",
        path=f"/restaurants/{id}",
        json_body=update_data,
    )