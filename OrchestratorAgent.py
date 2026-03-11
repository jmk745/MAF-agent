import os, asyncio
from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatClient
from agent_framework.agents import Handoff
import EmailAgent



# Retrieve Secrets
load_dotenv() 
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_PROJECT_ENDPOINT = os.getenv("GROK_PROJECT_ENDPOINT")


# Orchestrator Agent Factory
class OrchestratorAgent():
    
    def __init__(self,):

        # Gemini uses the OpenAI-compatible format
        gemini_client = OpenAIChatClient(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_PROJECT_ENDPOINT"),
            model_id="gemini-2.5-flash",
        )


        # 2. Create the Agent using the MAF class
        self = gemini_client.as_agent(
            name="Orchestrator Agent",
            instructions="You are a helpful orchestrator agent. " \
            "Use the available tools to assist the user.",

            tools=[Handoff(to=EmailAgent)]
        )