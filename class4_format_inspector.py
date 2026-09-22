import json
import logging
from pathlib import Path
import pandas as pd
import yaml
import os
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def inspect_csv(filepath):
    """Read a CSV file and display basic information."""
    df = pd.read_csv(filepath)
    logger.info(f"CSV file loaded from: {filepath}")
    logger.info(f"First three rows of the CSV file:\n{df.head(3)}")
    pass


def inspect_json(filepath):
    """Read a JSON file and display basic information."""
    
    with open(filepath, 'r') as file:
        data = json.load(file)
    logger.info(f"JSON file loaded from: {filepath}")
    logger.info(f"Contents of the JSON file:\n{data}")
    pass


def inspect_yaml(filepath):
    """Read a YAML file and display basic information."""
    
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)
    logger.info(f"YAML file loaded from: {filepath}")
    logger.info(f"Contents of the YAML file:\n{config}")
    pass


def inspect_env():
    """Read a .env file and display basic information."""
    load_dotenv()
    keys = [
        key for key in ["USERNAME", "PASSWORD"]
        if os.getenv(key) is not None
    ]

    # TODO:
    logger.info(".env file loaded.")
    logger.info(f"Keys found in .env: {keys}")
    pass

                

def main():
    # TODO:
    data_dir = Path("data")
    csv_path = data_dir / "sample.csv"
    json_path = data_dir / "sample.json"
    yaml_path = data_dir / "sample.yaml"

    inspect_csv(csv_path)
    inspect_json(json_path)
    inspect_yaml(yaml_path)
    inspect_env()

    pass


if __name__ == "__main__":
    main()
