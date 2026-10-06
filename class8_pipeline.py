import logging
from pathlib import Path
from class8_src import load_netflix, require_columns


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    input_path = Path("data/messy_netflix_titles.csv")

    # TODO 3:
    try:
        df = load_netflix(input_path)
        df = require_columns(df, ["title", "type", "release_year"])
        logger.info("Data validation passed. Proceeding with further processing...")
    except ValueError as e:
        logger.error(f"Data validation failed: {e}")
        exit(1)
    


if __name__ == "__main__":
    main()
