import logging

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