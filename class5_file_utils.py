import logging
from os import name, path
from pathlib import Path

logger = logging.getLogger(__name__)


def inspect_file(filepath_str):
    """Return basic information about an existing file."""
    path = Path(filepath_str)


    # TODO 2: If the path is not a file:
    if not path.is_file():
        logger.error(f"File not found: {filepath_str}")
        raise FileNotFoundError(f"File not found: {filepath_str}")

    # TODO 3: Return a dictionary containing:
    return {"name": path.name, "extension": path.suffix}

    


def inspect_extension(file_info):
    """Confirm that the file uses a supported text extension."""
    supported_extension = ".txt"

    # TODO 4: If file_info["extension"] does not equal
    if file_info["extension"] != supported_extension:
        logger.error(f"Unsupported file format: {file_info['extension']}")
        raise ValueError(f"Unsupported file format: {file_info['extension']}")
    

    # TODO 5: Return file_info.
    return file_info
    
