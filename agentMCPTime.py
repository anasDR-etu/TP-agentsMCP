import asyncio

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    client = MultiServerMCPClient(
        {
            "time": {
                "transport": "stdio",
                "command": "uvx",
                "args": [
                    "mcp-server-time",
                    "--local-timezone=Africa/Casablanca"
                ]
            }
        }
    )

    tools = await client.get_tools()

    print("Tools loaded:")
    print(tools)

    model = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )

    agent = create_agent(
        model=model,
        tools=tools
    )

    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content="What time is it in Japan?")
            ]
        }
    )

    print(response["messages"][-1].content)


asyncio.run(main())