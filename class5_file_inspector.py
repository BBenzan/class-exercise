import argparse
import logging
import sys

from class5_file_utils import inspect_file, inspect_extension

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a text file"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to a .txt file"
    )
    args = parser.parse_args()

    # TODO 1: Call inspect_file() inside a try block
    try:
        file = inspect_file(args.input)
    # TODO 2: Catch FileNotFoundError.
    except FileNotFoundError as e:
        logger.error(f"File not found: {args.input}")
        sys.exit(1)    

    # TODO 3: Call inspect_extension() inside a separate try block.
    try:
        file_info = inspect_extension(file)
    # TODO 4: Catch ValueError.
    except ValueError as e:
        logger.error(f"Unsupported file format: {file['extension']}")
        sys.exit(1)
    
    # TODO 5: Log an INFO message containing the
    logger.info(f"File information: {file_info}")



if __name__ == "__main__":
    main()
