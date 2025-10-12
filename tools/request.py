"""Request handling utilities."""

import requests


def send_request_and_get_response(
    url: str,
    method: str = "GET",
    headers: dict = None,
    formData: dict = None,
    data: dict = None,
    timeout: int = 60,
) -> dict:
    """Send an HTTP request and return the response content."""
    try:
        response = requests.request(
            method, url, headers=headers, data=formData, json=data, timeout=timeout
        )
        response.raise_for_status()  # Raise an error for bad responses
        return {"status_code": response.status_code, "content": response.text}
    except requests.RequestException as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": str(e)}


def download_file(
    url: str,
    file_path: str,
    method: str = "GET",
    headers: dict = None,
    formData: dict = None,
    timeout: int = 60,
) -> bytes:
    """Download a file from a URL and return its content as bytes."""
    try:
        response = requests.request(
            method, url, headers=headers, data=formData, timeout=timeout
        )
        response.raise_for_status()  # Raise an error for bad responses
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    except requests.RequestException as e:
        print(f"Error: {e}")
        return f"Error: {e}".encode()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"Unexpected error: {e}".encode()
