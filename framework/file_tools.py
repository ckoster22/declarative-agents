"""
Secure file operations for the declarative agent framework.

This module provides safe file reading and writing capabilities for agents,
with strict security measures to prevent directory traversal and unauthorized access.
"""

import tempfile
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Global temp directory for file operations
_TEMP_DIR: Optional[Path] = None


def _get_temp_dir() -> Path:
    """Get or create the dedicated temp directory for file operations."""
    global _TEMP_DIR
    if _TEMP_DIR is None:
        # Create a unique temp directory for this session
        _TEMP_DIR = Path(tempfile.mkdtemp(prefix="declarative_framework_"))
        logger.info(f"Created secure temp directory: {_TEMP_DIR}")
    return _TEMP_DIR


def _validate_filename(filename: str) -> None:
    if not filename:
        raise ValueError("Filename must be a non-empty string")

    if any(sep in filename for sep in ["/", "\\", ".."]):
        raise ValueError(
            "Filename cannot contain path separators or directory traversal"
        )

    dangerous_chars = ["<", ">", ":", '"', "|", "?", "*"]
    if any(char in filename for char in dangerous_chars):
        raise ValueError("Filename contains invalid characters")

    if len(filename) > 255:
        raise ValueError("Filename too long (max 255 characters)")

    if not filename.strip():
        raise ValueError("Filename cannot be empty or whitespace only")


def _get_secure_file_path(filename: str) -> Path:
    """
    Get a secure file path within the temp directory.

    Args:
        filename: The filename to create a path for

    Returns:
        Path object pointing to the file within the secure temp directory

    Raises:
        ValueError: If the filename is unsafe
    """
    _validate_filename(filename)
    temp_dir = _get_temp_dir()
    return temp_dir / filename


def read_file(filename: str) -> str:
    file_path = _get_secure_file_path(filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        logger.debug(f"Successfully read file: {filename}")
        return content
    except FileNotFoundError:
        logger.warning(f"File not found: {filename}")
        raise FileNotFoundError(f"File '{filename}' not found in temp directory")
    except UnicodeDecodeError as e:
        logger.error(f"Unicode decode error reading file {filename}: {e}")
        raise IOError(f"Unable to read file '{filename}': encoding error")
    except OSError as e:
        logger.error("OS error reading file %s: %s", filename, e)
        raise IOError(f"Error reading file '{filename}': {str(e)}")


def append_to_file(filename: str, content: str) -> str:
    file_path = _get_secure_file_path(filename)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)

        logger.debug(f"Successfully appended to file: {filename}")
        return f"Successfully appended content to file '{filename}' at: {file_path}"
    except OSError as e:
        logger.error("OS error appending to file %s: %s", filename, e)
        raise IOError(f"Error appending to file '{filename}': {str(e)}")


def get_temp_directory_info() -> str:
    temp_dir = _get_temp_dir()
    try:
        files = [f.name for f in temp_dir.iterdir() if f.is_file()]
        file_count = len(files)
        file_list = ", ".join(files) if files else "none"

        return f"Temp directory: {temp_dir}\nFiles in directory: {file_count} ({file_list})"
    except Exception as e:
        logger.error(f"Error getting temp directory info: {e}")
        return f"Temp directory: {temp_dir}\nError listing files: {str(e)}"
