"""
Secure file operations for the declarative agent framework.

This module provides safe file reading and writing capabilities for agents,
with strict security measures to prevent directory traversal and unauthorized access.
"""

import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class FileSystemManager:
    """Manages file system operations with encapsulated state."""

    def __init__(self):
        self._temp_dir: Path | None = None

    @property
    def temp_dir(self) -> Path:
        """Get or create the dedicated temp directory for file operations."""
        if self._temp_dir is None:
            # Create a unique temp directory for this session
            self._temp_dir = Path(tempfile.mkdtemp(prefix="declarative_framework_"))
            logger.info(f"Created secure temp directory: {self._temp_dir}")
        return self._temp_dir


# Global instance for backward compatibility
_file_system_manager = FileSystemManager()


def _get_temp_dir() -> Path:
    """Get or create the dedicated temp directory for file operations."""
    return _file_system_manager.temp_dir


def _validate_filename(filename: str) -> None:
    if not filename:
        raise ValueError("Filename must be a non-empty string")

    if any(sep in filename for sep in ["/", "\\", ".."]):
        raise ValueError("Filename cannot contain path separators or directory traversal")

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
    """Read a file from the secure temp directory.

    Args:
        filename: The filename to read

    Returns:
        The file contents as a string

    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file cannot be decoded as UTF-8
        OSError: If there's an OS-level error reading the file
    """
    file_path = _get_secure_file_path(filename)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    logger.debug(f"Successfully read file: {filename}")
    return content


def append_to_file(filename: str, content: str) -> str:
    """Append content to a file in the secure temp directory.

    Args:
        filename: The filename to append to
        content: The content to append

    Returns:
        A success message

    Raises:
        OSError: If there's an OS-level error writing to the file
    """
    file_path = _get_secure_file_path(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(content)

    logger.debug(f"Successfully appended to file: {filename}")
    return f"Successfully appended content to file '{filename}' at: {file_path}"


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
