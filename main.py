from dotenv import load_dotenv
from agent.py import *
import os






def main():

    agent = SimpleGroqAgent()
    output = agent.run("Hello Groq!")
    print(output)