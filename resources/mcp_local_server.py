from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local_server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.resource("info://langchain-mcp-adapters")
def library_info() -> str:
    return "langchain-mcp-adapters allows LangChain agents to use MCP tools, resources and prompts."

@mcp.prompt()
def prompt() -> str:
    return "You are a helpful assistant using MCP tools and resources."

if __name__ == "__main__":
    mcp.run()