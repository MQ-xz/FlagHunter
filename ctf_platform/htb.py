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

load_dotenv()
auth_token = os.getenv("HTB_AUTH_TOKEN")

htb_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "authorization": auth_token,
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


def get_challenge_info(challenge_url: str, type=None) -> dict:
    """Extract challenge ID from URL and fetch challenge info."""
    challenge_slug = challenge_url.rstrip("/").split("/")[-1]
    if type == "mechine":
        url = f'https://labs.hackthebox.com/api/v4/machine/profile/{challenge_slug}'
    else:
        url = f"https://labs.hackthebox.com/api/v4/challenge/info/{challenge_slug}"
    response = send_request_and_get_response(url, headers=htb_headers)
    return response


def download_challenge_file(challenge_id: int, filename: str) -> str:
    """Download a challenge file from HTB."""
    url = f"https://labs.hackthebox.com/api/v4/challenge/download/{challenge_id}"
    headers = htb_headers
    headers["accept"] = "application/octet-stream"
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    file_path = "downloads/" + filename
    return download_file(url, file_path, headers=headers)


def submit_flag(challenge_id: int, flag: str, difficulty: int = 10, type=None) -> dict:
    """Submit a flag to the Hack The Box platform."""
    if type == "mechine":
        url = "https://labs.hackthebox.com/api/v5/machine/own"
        data = {"flag": flag, "id": challenge_id}
    else:
        url = "https://labs.hackthebox.com/api/v4/challenge/own"
        data = {"flag": flag, "difficulty": difficulty, "challenge_id": challenge_id}
    response = send_request_and_get_response(
        url, method="POST", headers=htb_headers, data=data
    )
    return response


def start_container_instance(challenge_id: int, type=None) -> dict:
    """Start a container instance for a challenge."""
    if type == "mechine":
        url = "https://labs.hackthebox.com/api/v4/vm/spawn"
        data = {"machine_id": challenge_id}
    else:
        url = "https://labs.hackthebox.com/api/v4/challenge/start"
        data = {"challenge_id": challenge_id}
    response = send_request_and_get_response(
        url, method="POST", headers=htb_headers, data=data
    )
    return response


def stop_container_instance(challenge_id: int, type=None) -> dict:
    """Stop a container instance for a challenge."""
    if type == "mechine":
        url = "https://labs.hackthebox.com/api/v4/vm/terminate"
        data = {"machine_id": challenge_id}
    else:
        url = "https://labs.hackthebox.com/api/v4/challenge/stop"
        data = {"challenge_id": challenge_id}
    response = send_request_and_get_response(
        url, method="POST", headers=htb_headers, data=data
    )
    return response


TOOLS = [
    get_challenge_info,
    download_challenge_file,
    submit_flag,
    start_container_instance,
    stop_container_instance,
    read_file,
    write_file,
    change_file_permissions,
    list_directory_contents,
    extract_zip_file,
    execute_command,
    send_request_and_get_response,
    download_file,
]

OS_INFO = {
    "os": os.name,
    "platform": os.sys.platform,
}

SYSTEM_PROMPT = """You are an expert penetration tester using the Hack The Box (HTB) platform. When provided with an HTB challenge URL, follow this workflow:

Your system information is as follows:
{os_info}


1. Extract the challenge information from the URL using get_challenge_info(). based on the challenge type (normal or mechine) pass the type parameter accordingly.
2. Analyze the challenge description to identify key objectives and requirements.
3. Based on the play_methods in the challenge information:
   a) If BOTH download AND container are available:
      - Download challenge files using download_challenge_file()
      - Extract with password "hackthebox" to `extract/<challenge_id>` directory
      - Analyze files for vulnerabilities and functionality
      - Start a container instance with start_container_instance()
      - Get updated challenge info for connection details (play_info.ip and play_info.port)
   
   b) If ONLY container is available:
      - Start a container instance with start_container_instance()
      - Get updated challenge info for connection details (play_info.ip and play_info.port)
   
   c) If ONLY download is available:
      - Download challenge files using download_challenge_file()
      - Extract with password "hackthebox"  to `extract/<challenge_id>` directory
      - Analyze files for vulnerabilities and functionality

4. Utilize available tools:
   - For OS commands: execute_command()
   - For file operations: read_file(), write_file(), etc.
   - For network requests: send_request_and_get_response()
   - Install additional tools as needed using execute_command()

5. For custom exploits:
   - Create files using write_file() in the exploits/<challenge_id> directory
   - Set permissions with change_file_permissions()
   - Execute with execute_command()

6. Submit the discovered flag (format "HTB{...}") using submit_flag(). if you get 403 on submiting flag this mean the flag is incorrect so dont try to submit the same flag again and again. instead retry the whole process again to find the correct flag.

- Always approach challenges methodically, thinking step-by-step.
- Don't make up your own flags and try to submit, only submit when you are sure you have the correct flag.
- Ensure proper parameter usage with all functions.
- Dont call API functions multiple times unnecessarily, bcz it may lead to rate limiting or unexpected behavior. so call them only when needed. else check history or previous responses.
- if you are downloading any file or tool use downloads/ directory to save it.
"""


def start_hacking(agent):
    # get argument from command line
    type = "mechine" if "machines" in challenge_url else "challenge"
    # remove url encoding like spaces %2520
    challenge_url = challenge_url.replace("%2520", " ")
    print(f"Challenge URL: {challenge_url}")
    task = f"Get the challenge info from this url: {challenge_url}\nChallenge type: {type}\n\n your task is to go the challenge, find the flag and submit it using submit_flag() function. if you get 403 on submiting flag this mean the flag is incorrect so dont try to submit the same flag again and again. instead retry the whole process again to find the correct flag."
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": task}]},
        {"recursion_limit": 200},
        stream_mode="updates",
    ):
        for step, data in chunk.items():
            print(f"step: {step}")
            print(f"content: {data['messages'][-1].content_blocks}")
