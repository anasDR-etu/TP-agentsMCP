import asyncio

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    client = MultiServerMCPClient(
        {
            "local_server": {
                "transport": "stdio",
                "command": "python",
                "args": ["resources/mcp_local_server.py"],
            }
        }
    )

    tools = await client.get_tools()
    resources = await client.get_resources("local_server")

    prompt = await client.get_prompt("local_server", "prompt")
    system_prompt = prompt[0].content

    print("Resources:")
    print(resources)

    model = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt
    )

    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content="Use the tool to calculate 10 + 25")
            ]
        }
    )

    print(response["messages"][-1].content)


asyncio.run(main())