import os, asyncio
from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatClient
import tools
from userMemoryProvider import UserMemoryProvider



load_dotenv() 
# Retrieve Secrets
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_PROJECT_ENDPOINT = os.getenv("GROK_PROJECT_ENDPOINT")


async def main():

    # Gemini uses the OpenAI-compatible format
    gemini_client = OpenAIChatClient(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url=os.getenv("GEMINI_PROJECT_ENDPOINT"),
        model_id="gemini-2.5-flash",
    )


    # 2. Create the Agent using the MAF class
    my_agent = gemini_client.as_agent(
        name="Will, the WeatherAgent",
        instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
        tools=tools.get_weather,
        context_providers=[UserMemoryProvider()]
    )

    my_session = my_agent.create_session()

    my_session = my_agent.create_session()


    # 3. Execute a task
    # # First turn — the agent should remember the user's name and hobby
    result = await my_agent.run("My name is Emily and I like to hike.", session=my_session)
    print(f"Agent Response: {result}")
    
    # Second turn — the agent should remember the user's name and hobby
    result = await my_agent.run("What do you remember about me?", session=my_session)
    print(f"Agent Response: {result}")
    # # First turn — the agent should remember the user's name and hobby
    result = await my_agent.run("My name is Emily and I like to hike.", session=my_session)
    print(f"Agent Response: {result}")
    
    # Second turn — the agent should remember the user's name and hobby
    result = await my_agent.run("What do you remember about me?", session=my_session)
    print(f"Agent Response: {result}")

    # Third turn — the agent should remember the user's name and hobby
    result = await my_agent.run("I want to hike in New York. How's the weather there?", session=my_session)
    print(f"Agent Response: {result}")

    provider_state = my_session.state.get("user_memory", {})
    print(f"[Session State] Stored user name: {provider_state.get('location')}")




if __name__ == "__main__":
    asyncio.run(main())
    