import logging
import re
import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.info("Displaying DataFrame overview.")
    # TODO 1:
    logger.debug(f"DataFrame shape: {df.shape}")
    print(f"DataFrame first five rows: {df.head()}")
    print(f"DataFrame column names: {df.columns.tolist()}")
    print(f"DataFrame data types: {df.dtypes}")

    pass


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    logger.info("Removing duplicate rows.")
    # TODO 2:
    before_count = df.shape[0]
    df = df.drop_duplicates()
    after_count = df.shape[0]
    logger.debug(f"Duplicate rows removed: {before_count - after_count}")
    return df
    


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    # TODO 3:
    logger.info("Dropping rows with missing values.")
    before_count = df.shape[0]
    df = df.dropna()
    after_count = df.shape[0]
    logger.debug(f"Rows with missing values removed: {before_count - after_count}")
    return df

def clean_text(value):
    """Normalize one text value."""
    # TODO 1:
    value = str.strip(value)  # Remove leading/trailing whitespace
    value = value.lower()  # Convert to lowercase
    value = clean_text(value)  # Remove extra whitespace
    

def clean_text(text):
    text = text.strip()
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    # TODO 2:
    # If column does not exist:
    if column not in df.columns:
        logger.error(f"Column '{column}' does not exist in the DataFrame.")
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    # Calculate Q1, Q3, and IQR.
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Use threshold to calculate lower and upper bounds.
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    # Keep rows inside the bounds.
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    # Log a DEBUG message containing the bounds and the number of rows removed.
    logger.debug(f"Column '{column}': Lower bound = {lower_bound}, Upper bound = {upper_bound}")
    logger.debug(f"Rows removed: {df.shape[0] - df_filtered.shape[0]}")

    # Return the resulting DataFrame.
    return df_filtered
    