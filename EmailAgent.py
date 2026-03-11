import os, asyncio
from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatClient
import gmailTools
from userMemoryProvider import UserMemoryProvider


# Retrieve Secrets
load_dotenv()



# Email Agent
class EmailAgent():
    
    def __init__(self):

        # Gemini uses the OpenAI-compatible format
        gemini_client = OpenAIChatClient(
            api_key=os.getenv("HUGGINGFACE_API_KEY"),
            base_url=os.getenv("HUGGINGFACE_PROJECT_ENDPOINT"),
            model_id=os.getenv("HUGGINGFACE_MODEL_ID"),
        )


        # 2. Create the Agent using the MAF class
        self.agent = gemini_client.as_agent(
            name="Eddy, the Email Agent",
            instructions="You are an email agent that is specialized in managing Gmail communications for the user. " \
            "Use the available tools to assist the user with reading and sending emails. " \
            "Always ask the user for confirmation before sending an email, " \
            "and summarize the content of emails you read to the user, "
            "and ask if they want to reply." \
            "If you are unsure about what the user wants, ask clarifying questions." \
            "If you are requested to check emails, access their gmail inbox and summarize any new messages, especially those from contacts the user frequently communicates with.   ",
            tools=[gmailTools.read_emails, gmailTools.send_gmail_message]
        )

    async def __call__(self, user_input):
        # This allows you to treat the object like a function
        return await self.agent.run(user_input)