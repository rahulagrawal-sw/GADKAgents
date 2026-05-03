from mcp.server.fastmcp import FastMCP


mcp_server = FastMCP(name = "weather_mcp_server")

@mcp_server.tool()
def get_weather(city: str) -> str:
    print(f"get_weather is called for {city}")
    return f"The weather in {city} is sunny"

if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")