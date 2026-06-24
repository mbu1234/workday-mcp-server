import os
from mcp.server.fastmcp import FastMCP

from .tools.restaurants import list_restaurants

mcp = FastMCP("Workday MCP Server")


@mcp.tool(
    name="list_restaurants",
    description="Returns the list of restaurants from the Workday REST API."
)
async def list_restaurants_tool():
    return await list_restaurants()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        path="/mcp",
    )