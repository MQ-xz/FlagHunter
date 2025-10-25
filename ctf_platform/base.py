import os
import logging
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pydantic import BaseModel
from dotenv import load_dotenv

from tools.os_commands import execute_command
from tools.file_operations import (
    read_file,
    write_file,
    change_file_permissions,
    list_directory_contents,
    extract_zip_file,
)
from tools.request import send_request_and_get_response, download_file


load_dotenv()

BASE_TOOLS = [
    execute_command,
    read_file,
    write_file,
    change_file_permissions,
    list_directory_contents,
    extract_zip_file,
    send_request_and_get_response,
    download_file,
]


class ChallengeSolvedFormat(BaseModel):
    challenge_id: str
    flag: str


class BasePlatform:

    def __init__(self, system_prompt: str, tools: list):
        self.llm_model = ChatOpenAI(
            model=os.getenv("AI_MODEL"),
            api_key=os.getenv("AI_API_KEY"),
            base_url=os.getenv("AI_BASE_URL"),
        )
        self.agent = create_agent(
            model=self.llm_model,
            tools=BASE_TOOLS + tools,
            system_prompt=system_prompt,
            response_format=ChallengeSolvedFormat,
        )
        self.logger = self.get_logger("BasePlatform")

    def get_system_prompt(self, system_prompt) -> str:
        """Return the system prompt for the platform."""
        return f"""You are a professional Capture The Flag (CTF) player. going around the world and participating in CTF competitions. participating each competition helps you to improve your skills and gain more experience in the field of cybersecurity.
        
        {system_prompt}

        When solving a CTF challenge, follow these steps:
        Utilize available tools:
        - For OS commands: execute_command()
        - For file operations: read_file(), write_file(), etc.
        - For network requests: send_request_and_get_response()
        - Install additional tools as needed using execute_command()

        For custom exploits:
        - Create files using write_file() in the challenges/<challenge_id>/exploits/ directory
        - Set permissions with change_file_permissions()
        - Execute with execute_command()

        Submit the discovered flag using submit_flag(). if you get any error on submitting flag this mean the flag is incorrect so dont try to submit the same flag again and again. instead retry the whole process again to find the correct flag.

        Things to keep in mind:
        - Always approach challenges methodically, thinking step-by-step.
        - Don't make up your own flags and try to submit, only submit when you are sure you have the correct flag.
        - Don't call API functions multiple times unnecessarily, because it may lead to rate limiting or unexpected behavior. So call them only when needed. Else check history or previous responses.
        - If challenge has any file or attachment, it should be saved in the challenges/<challenge_id>/ directory, also if you are writing any exploit or script for the challenge, you can use the same directory to save your files.
        - When ever using filepaths or directory paths, make sure to added challenges/<challenge_id>/ as prefix to the path. to ensure you are working within the challenge workspace.
        """

    def get_logger(self, challenge: str):
        """Get a logger for the specific challenge."""

        logger = logging.getLogger(f"Challenge.{challenge}")
        if not os.path.exists("logs"):
            os.makedirs("logs")
        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(f"logs/Challenge_{challenge}.log")

            console_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.addHandler(console_handler)
        return logger

    def solve_challenge(self, task: str, headers: dict = None):
        """Start the challenge solving process."""
        try:
            for chunk in self.agent.stream(
                {"messages": [{"role": "user", "content": task}]},
                {"recursion_limit": 200, "configurable": {"headers": headers}},
                stream_mode="updates",
            ):
                # Each chunk contains the full state at that point
                for step, data in chunk.items():
                    self.logger.info(f"step: {step}")
                    self.logger.info(f"content: {data['messages'][-1].content_blocks}")
        except Exception as e:
            self.logger.error(f"Error during challenge solving: {e}")
        self.logger.info("Challenge solving process completed.")
