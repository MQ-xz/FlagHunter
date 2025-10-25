"""HTB related tools"""

import os
import sys
from dotenv import load_dotenv
from tools.request import send_request_and_get_response, download_file
from tools.file_operations import (
    read_file,
    write_file,
    change_file_permissions,
    list_directory_contents,
    extract_zip_file,
)
from tools.os_commands import execute_command
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
import json

load_dotenv()
auth_token = os.getenv("HTB_AUTH_TOKEN")

htb_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "origin": "https://app.hackthebox.com",
    "priority": "u=1, i",
    "referer": "https://app.hackthebox.com/",
    "sec-ch-ua": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
}


def get_headers() -> dict:
    """Generate HTB headers with authentication token."""
    headers = HEADERS.copy()
    headers["authorization"] = os.getenv("HTB_AUTH_TOKEN")
    return headers


def clean_challenge_url(challenge_url: str) -> str:
    """Clean and standardize the challenge URL."""
    return challenge_url.replace("%2520", " ")


def get_challenge_info(
    challenge_url: str, header: dict, challenge_type: str | None = None
) -> dict:
    """Extract challenge ID from URL and fetch challenge info."""
    challenge_url = clean_challenge_url(challenge_url)
    challenge_slug = challenge_url.rstrip("/").split("/")[-1]
    if challenge_type == "machine":
        url = f"https://labs.hackthebox.com/api/v4/machine/profile/{challenge_slug}"
    else:
        url = f"https://labs.hackthebox.com/api/v4/challenge/info/{challenge_slug}"
    response = request_and_respond(url, headers=header)
    return response.get("challenge", {})


def download_challenge_attachment(challenge_id: int, header: dict) -> None:
    """Download challenge attachment."""
    url = f"https://labs.hackthebox.com/api/v4/challenge/download/{challenge_id}"
    download_result = request_and_respond(url, headers=header, response_type="content")
    workspace = f"challenges/{challenge_id}/"
    file_name = "attachment.zip"
    file_path = os.path.join(workspace, file_name)
    if not os.path.exists(workspace):
        os.makedirs(workspace)
    with open(file_path, "wb") as file:
        file.write(download_result)
    extract_zip(
        zip_path=file_path,
        extract_to=f"{workspace}/extracted/",
        password="hackthebox",
    )


@tool
def submit_flag(
    challenge_id: int,
    flag: str,
    difficulty: int = 10,
    challenge_type=None,
    config: RunnableConfig = None,
) -> dict:
    """Submit a flag to the Hack The Box platform."""
    if challenge_type == "machine":
        url = "https://labs.hackthebox.com/api/v5/machine/own"
        data = {"flag": flag, "id": challenge_id}
    else:
        url = "https://labs.hackthebox.com/api/v4/challenge/own"
        data = {"flag": flag, "difficulty": difficulty, "challenge_id": challenge_id}
    response = request_and_respond(
        url=url, method="POST", headers=config["configurable"]["headers"], data=data
    )
    return response


@tool
def start_container_instance(
    challenge_id: int, challenge_type=None, config: RunnableConfig = None
) -> dict:
    """Start a container instance for a challenge."""
    if challenge_type == "machine":
        url = "https://labs.hackthebox.com/api/v4/vm/spawn"
        data = {"machine_id": challenge_id}
    else:
        url = "https://labs.hackthebox.com/api/v4/challenge/start"
        data = {"challenge_id": challenge_id}
    response = request_and_respond(
        url=url, method="POST", headers=config["configurable"]["headers"], data=data
    )
    return response


@tool
def stop_container_instance(
    challenge_id: int, challenge_type=None, config: RunnableConfig = None
) -> dict:
    """Stop a container instance for a challenge."""
    if challenge_type == "machine":
        url = "https://labs.hackthebox.com/api/v4/vm/terminate"
        data = {"machine_id": challenge_id}
    else:
        url = "https://labs.hackthebox.com/api/v4/challenge/stop"
        data = {"challenge_id": challenge_id}
    response = request_and_respond(
        url=url, method="POST", headers=config["configurable"]["headers"], data=data
    )
    return response


@tool
def get_container_info(
    challenge_url: str, challenge_type=None, config: RunnableConfig = None
) -> dict:
    """Get container instance info for a challenge."""
    challenge_info = get_challenge_info(
        challenge_url,
        header=config["configurable"]["headers"],
        challenge_type=challenge_type,
    )
    return challenge_info.get("play_info", {})


TOOLS = [
    submit_flag,
    start_container_instance,
    stop_container_instance,
    get_container_info,
]


SYSTEM_PROMPT = """You currently trying to solve a HackTheBox challenge. follow the steps below to solve the challenge:

FLAG FORMAT: HTB{{...}}

1. Analyze the challenge name, description, category, difficulty and any other available information to understand what is required to solve it.
2. Check if user provided any files or attachments related to the challenge. If yes, please analyze them to understand their purpose, how they work, and if they contain any vulnerabilities that can be exploited.
3. If the challenge contains a container as well then follow the steps:
    a. Start the container instance using start_container_instance() tool.
    b. Get the container connection details using get_container_info() tool.
4. Based on the challenge type and available information, plan your approach to solve the challenge. This may involve:
"""


def start_hacking(agent):
    # get argument from command line
    try:
        challenge_url = sys.argv[1]
    except IndexError:
        challenge_url = input("Enter the challenge URL: ")
    challenge_type = "machine" if "machines" in challenge_url else "challenge"
    # remove url encoding like spaces %2520
    challenge_url = challenge_url.replace("%2520", " ")
    print(f"Challenge URL: {challenge_url}")
    task = f"Get the challenge info from this url: {challenge_url}\nChallenge type: {type}\n\n your task is to go the challenge, find the flag and submit it using submit_flag() function. if you get 403 on submiting flag this mean the flag is incorrect so dont try to submit the same flag again and again. instead retry the whole process again to find the correct flag."
    console = Console()

    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": task}]},
        {"recursion_limit": 200},
        stream_mode="updates",
    ):
        for step, data in chunk.items():
            # Step as a styled title panel
            console.print()
            console.rule(f"[bold cyan]⚡ Step: {step}[/bold cyan]", style="cyan")

            messages = data.get("messages", [])
            if not messages:
                continue

            content_blocks = messages[-1].content_blocks
            if not content_blocks:
                continue

            # Build table
            table = Table(
                box=box.ROUNDED,
                show_header=True,
                header_style="bold magenta",
                border_style="dim cyan",
                expand=True,
                padding=(0, 1),
            )
            table.add_column("Type", style="bold yellow", width=12, no_wrap=True)
            table.add_column("Name / ID", style="cyan", width=24)
            table.add_column("Content", style="white")

            for block in content_blocks:
                block_type = block.get("type", "unknown")

                if block_type == "text":
                    text = block.get("text", "")
                    table.add_row(
                        "[green]📝 text[/green]",
                        "—",
                        Text(text, overflow="fold"),
                    )

                elif block_type == "tool_call":
                    name = block.get("name", "")
                    call_id = block.get("id", "")
                    args = block.get("args", {})
                    args_str = json.dumps(args, indent=2)
                    table.add_row(
                        "[blue]🔧 tool_call[/blue]",
                        f"[bold]{name}[/bold]\n[dim]{call_id}[/dim]",
                        Text(args_str, overflow="fold"),
                    )

                else:
                    table.add_row(
                        f"[dim]{block_type}[/dim]",
                        "—",
                        Text(str(block), overflow="fold"),
                    )

            console.print(table)
