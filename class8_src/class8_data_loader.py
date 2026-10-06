import logging
import pandas as pd

logger = logging.getLogger(__name__)

def load_netflix(filepath):
    """Load the Netflix CSV file."""
    # TODO 1:
    df = pd.read_csv(filepath)
    logger.info(f"Loaded data from {filepath} with shape {df.shape}.")
    return df
   
