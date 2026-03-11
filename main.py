import asyncio
from agents import Session
from dotenv import load_dotenv
import os
import EmailAgent





async def main():
    
    email_agent = EmailAgent.EmailAgent()
    #session = Session(agent=email_agent)
    
    
    user_input = "Can you check my recent emails?"
    
    response = await email_agent(user_input)
    print(f"Agent Response: {response}")







if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user.")