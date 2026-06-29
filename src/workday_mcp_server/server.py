import os

from mcp.server.fastmcp import FastMCP

from workday_mcp_server.tools.restaurants import list_restaurants


mcp = FastMCP("Workday MCP Server")


@mcp.tool()
async def list_restaurants_tool():
    """
    Returns the list of restaurants from the Workday REST API.
    """
    return await list_restaurants()


if __name__ == "__main__":
    # Configure Streamable HTTP transport
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.getenv("PORT", "8000"))
    mcp.settings.streamable_http_path = "/mcp"

    print(f"Starting MCP server on http://0.0.0.0:{mcp.settings.port}/mcp")

    mcp.run(transport="streamable-http")