import os
from dotenv import load_dotenv
import asyncio
from agent_framework import Agent
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
        model_id="llama-3.3-70b-versatile" # Or your preferred Groq model
    )


    # 2. Create the Agent using the MAF class
    # You no longer need to manually define 'run' or 'call_api'
    my_agent = Agent(
        name="WeatherAgent",
        client=groq_client,
        instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
        tools=tools.get_weather,
    )


    # 3. Execute a task
    result = await my_agent.run("What is the weather in New York?")
    print(f"Agent Response: {result.messages[-1].text}")







if __name__ == "__main__":
    asyncio.run(main())