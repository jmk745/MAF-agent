import os
from dotenv import load_dotenv
import asyncio
from agent_framework.openai import OpenAIChatClient

import tools  # Import your tools here (e.g., from tools import get_weather)



load_dotenv() 
# Retrieve Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_PROJECT_ENDPOINT = os.getenv("GROQ_PROJECT_ENDPOINT")


async def main():

    # 1. Configure the Client for Groq
    # Groq uses the OpenAI-compatible format
    groq_client = OpenAIChatClient(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        model_id="llama-3.3-70b-versatile", # Or your preferred Groq model
    )


    # 2. Create the Agent using the MAF class
    # You no longer need to manually define 'run' or 'call_api'
    my_agent = groq_client.as_agent(
        name="Will, the WeatherAgent",
        instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
        tools=tools.get_weather,
    )

    my_session = my_agent.create_session()


    # 3. Execute a task
    # # First turn — the agent should remember the user's name and hobby
    result = await my_agent.run("My name is Emily and I like to hike.", session=my_session)
    print(f"Agent Response: {result}")
    
    # Second turn — the agent should remember the user's name and hobby
    result = await my_agent.run("What do you remember about me?", session=my_session)
    print(f"Agent Response: {result}")

    # Third turn — the agent should remember the user's name and hobby
    result = await my_agent.run("I want to hike in New York. How's the weather there?", session=my_session)
    print(f"Agent Response: {result}")




if __name__ == "__main__":
    asyncio.run(main())
    