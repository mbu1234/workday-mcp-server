import os

from mcp.server.fastmcp import FastMCP

from workday_mcp_server.tools.restaurants import list_restaurants
from workday_mcp_server.tools.restaurant_orders import list_restaurant_orders
from workday_mcp_server.tools.get_restaurant_orders_wql import (
    get_restaurant_orders_wql,
)
from workday_mcp_server.tools.patch_restaurant import patch_restaurant
from workday_mcp_server.tools.get_worker_by_name import (
    get_worker_by_name,
)
from workday_mcp_server.tools.post_restaurant_order import (
    post_restaurant_order,
)
from workday_mcp_server.tools.delete_restaurant_order import (
    delete_restaurant_order,
)


mcp = FastMCP("Workday MCP Server")


@mcp.tool()
async def list_restaurants_tool():
    """
    Returns the list of restaurants from the Workday REST API.
    """
    return await list_restaurants()


@mcp.tool()
async def list_restaurant_orders_tool():
    """
    Returns the list of restaurant orders from the Workday REST API.
    """
    return await list_restaurant_orders()


@mcp.tool()
async def get_restaurant_orders_wql_tool():
    return await get_restaurant_orders_wql()


@mcp.tool()
async def patch_restaurant_tool(
    id: str,
    name: str,
    type: str,
    active: bool,
):
    return await patch_restaurant(id, name, type, active)


@mcp.tool()
async def get_worker_by_name_tool(
    worker_name: str,
):
    return await get_worker_by_name(worker_name)


@mcp.tool()
async def post_restaurant_order_tool(
    restaurant_id: str,
    worker_id: str,
    order_items_input: str,
    delivery_date: str,
    order_address: str,
):
    return await post_restaurant_order(
        restaurant_id,
        worker_id,
        order_items_input,
        delivery_date,
        order_address,
    )


@mcp.tool()
async def delete_restaurant_order_tool(id: str):
    return await delete_restaurant_order(id)



if __name__ == "__main__":
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.getenv("PORT", "8000"))
    mcp.settings.streamable_http_path = "/mcp"

    # Required for Render public URL.
    mcp.settings.transport_security.enable_dns_rebinding_protection = False

    print(f"Starting MCP server on http://0.0.0.0:{mcp.settings.port}/mcp")

    mcp.run(transport="streamable-http")