import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    drop_missing_rows,
    remove_duplicates,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # TODO 4:
    path = Path(args.input)
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        sys.exit(1)
    logger.info(f"DataFrame loaded successfully from {path}")

    # TODO 5:
    show_overview(df)
    logger.info("Overview displayed successfully.")
   
    # TODO 6:
    df_rows_before = df.shape[0]
    removed_duplicates_df = remove_duplicates(df)
    df_rows_after = removed_duplicates_df.shape[0]

    logger.info(f"{df_rows_before - df_rows_after} duplicate rows removed.")
    
    dropped_missing_df = drop_missing_rows(removed_duplicates_df)
    df_rows_after2 = dropped_missing_df.shape[0]
    logger.info(f"{df_rows_after - df_rows_after2} rows with missing values dropped.")
    
    logger.info(f"Final DataFrame shape: {dropped_missing_df.shape}")
    logger.info(f"total rows removed: {df_rows_before - df_rows_after2}")

if __name__ == "__main__":
    main()
