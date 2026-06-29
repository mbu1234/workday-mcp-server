import os

from mcp.server.fastmcp import FastMCP

from workday_mcp_server.tools.restaurants import list_restaurants
from workday_mcp_server.tools.restaurant_orders import list_restaurant_orders
from workday_mcp_server.tools.get_restaurant_orders_wql import (
    get_restaurant_orders_wql,
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


if __name__ == "__main__":
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.getenv("PORT", "8000"))
    mcp.settings.streamable_http_path = "/mcp"

    # Required for Render public URL.
    mcp.settings.transport_security.enable_dns_rebinding_protection = False

    print(f"Starting MCP server on http://0.0.0.0:{mcp.settings.port}/mcp")

    mcp.run(transport="streamable-http")