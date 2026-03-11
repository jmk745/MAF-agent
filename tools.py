from agent_framework import *
from random import randint, choice
from typing import Annotated

# NOTE: approval_mode="never_require" is for sample brevity.
# Use "always_require" in production for user confirmation before tool execution.


@tool(approval_mode="never_require")
def get_weather(location: str):
    # conditions = ["sunny", "cloudy", "rainy", "stormy"]
    # weather = choice(conditions)
    # temperature = randint(10, 30)
    # return f"The weather in {location} is {weather} with a high of {temperature}°C."
    return "It's sunny and 25°C in New York City today!"