import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client



from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

async def main():
    model = ChatOpenAI(model="gpt-4o")

    server_params = StdioServerParameters(
        command="python",
        args=["spotify-mcp/src/spotify_mcp/server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print("🛠 Tools loaded.")

            agent = create_react_agent(model, tools)

            while True:
                user_input = await asyncio.to_thread(input, "\n🗣️  Your message (type 'exit' to quit): ")

                if user_input.strip().lower() in ["exit", "quit"]:
                    print("👋 Exiting.")
                    break

                agent_response = await agent.ainvoke({"messages": user_input})
                print(f"🤖 Response:\n{agent_response['messages'][-1].content}\n")

if __name__ == "__main__":
    asyncio.run(main())