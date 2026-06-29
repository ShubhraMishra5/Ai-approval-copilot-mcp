import asyncio
from fastmcp import Client

async def main():

    async with Client("./chatbot_mcp/mcp_server.py") as client:

        tools = await client.list_tools()

        print("TOOLS:")
        print(tools)

        result = await client.call_tool(
            "run_select_query",
            {
                "query": "SELECT COUNT(*) FROM approval_requests"
            }
        )

        print("\nRESULT:")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())