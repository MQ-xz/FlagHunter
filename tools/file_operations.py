"""File or directory operations."""

import os
import zipfile


def read_file(file_path: str) -> str:
    """Read the content of a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"


def write_file(file_path: str, content: str) -> None:
    """Write content to a file."""
    _dir = os.path.dirname(file_path)
    if _dir and not os.path.exists(_dir):
        os.makedirs(_dir)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        return f"Error writing file {file_path}: {e}"


def change_file_permissions(file_path: str, permissions: int) -> None:
    """Change the permissions of a file."""
    try:
        os.chmod(file_path, permissions)
    except Exception as e:
        return f"Error changing permissions for file {file_path}: {e}"


def list_directory_contents(directory_path: str) -> list:
    """List the contents of a directory."""
    try:
        items = []
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                items.append(f"{item}/ (directory)")
            else:
                items.append(f"{item} (file)")
        return items
    except Exception as e:
        return f"Error listing directory contents for {directory_path}: {e}"


def extract_zip_file(zip_path: str, extract_to: str, password: str = None) -> None:
    """Extract a zip file to a specified directory."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            if password is None:
                zip_ref.extractall(extract_to)
            else:
                zip_ref.extractall(extract_to, pwd=password.encode())
    except Exception as e:
        return f"Error extracting zip file {zip_path}: {e}"
