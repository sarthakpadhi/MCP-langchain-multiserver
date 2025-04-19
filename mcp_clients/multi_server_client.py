from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio


from langchain_openai import ChatOpenAI



load_dotenv()
async def main():
    model = ChatOpenAI(model="gpt-4o")
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["math_server/math_server.py"],
                "transport": "stdio",
            },
            "spotify": {
                "command": "python",
                "args" : ["spotify-mcp/src/spotify_mcp/server.py"],
                "transport": "stdio",
            }
        }
    ) as client:
        tools = client.get_tools()
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
        
