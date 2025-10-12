"""Main entry point for the agent."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from ctf_platform.htb import TOOLS, SYSTEM_PROMPT, start_hacking

# Load environment variables from .env file
load_dotenv()

# Initialize the ChatOpenAI model with environment variables
llm_model = ChatOpenAI(
    model=os.getenv("AI_MODEL"),
    api_key=os.getenv("AI_API_KEY"),
    base_url=os.getenv("AI_BASE_URL"),
)


# Create an agent with the LLM model and the weather tool
agent = create_agent(
    model=llm_model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)


if __name__ == "__main__":
    start_hacking(agent)
