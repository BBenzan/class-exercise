import pandas as pd
import pytest  # type: ignore

from class10_data_validator import validate_columns

@pytest.fixture
def sample_df():
    """Create a small DataFrame for testing."""
    return pd.DataFrame(
        {
            "title": ["Movie A", "Movie B"],
            "type": ["Movie", "Movie"],
            "release_year": [2020, 2021],
        }
    )


def test_validate_columns_with_valid_columns(sample_df):
    # TODO 1:
    
    # Arrange the required column names.
    required_columns = ["title", "type", "release_year"]
    # Act by calling validate_columns().
    result = validate_columns(sample_df, required_columns)
    # Assert that the returned DataFrame has the expected columns.
    assert list(result.columns) == required_columns


def test_validate_columns_with_missing_column(sample_df):
    # TODO 2:
    # Use pytest.raises() to confirm that validate_columns()
    # raises ValueError when a required column is missing.
    with pytest.raises(ValueError):
        validate_columns(sample_df, ["title", "type", "wrong_column"])
