# Weekly Announcements
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
* **Quiz Score on Canvas (Quizzes 1-5 Only)**
    - Your current Quiz grade is based on Quizzes 1–5. Please review your current standing and use it to plan for the upcoming quizzes -- there are 5 remaining quizzes, plus 1 optional quiz.
    - Note: 
        - At the end of the semester, we will update this grade one final time, capping the quiz score at 5,400 points. Following the quiz policy, any points earned beyond 5,400, where applicable, will be converted into bonus points and recorded in a separate column.
        - If you earn bonus points, they will appear in that column. A comment in the same column will show your total quiz points and provide a breakdown of how those points are allocated.
* **MP2 next week:** Our second MP will be availabile starting next week. We will spend two weeks covering MP2. 

---

# Class 11: Testing MP1

## Learning Objectives

By the end of today's class, you will be able to:

1. Organize tests for a multi-module project.
    1. Share fixtures through `conftest.py`.
    2. Use `tmp_path` to test file output safely.
2. Test normal and error behavior in MP1.

---

# Before We Begin

1. Open your `mp1-data-pipeline` repository and activate its virtual environment.

2. Create a feature branch:

```bash
git switch -c feature/pytest
```

3. Install pytest, then update `requirements.txt`:

```bash
python -m pip install pytest
python -m pip freeze > requirements.txt
```

4. Create the following test structure:

```text
mp1-data-pipeline/
├── tests/                      (new)
│   ├── conftest.py             (new; empty for now)
│   ├── test_data_validator.py  (new; empty for now)
│   ├── test_data_processor.py  (new; empty for now)
│   └── test_data_output.py     (new; empty for now)
├── pipeline.py
├── src/
│   └── ...
│   ...

```

We will run all commands from the repository root so the fixture can find `fixtures/sample_data.csv`.

---

# Part 1: What Should We Test in a Project (e.g., MP1)? (quiz)

MP1 contains several modules with different responsibilities:

| Module | Example Behavior to Test |
| :--- | :--- |
| Data loader | Returns the expected data for a supported file |
| Data validator | Rejects missing columns or removes invalid values |
| Data processor | Removes or preserves the expected rows |
| Data output | Creates a CSV file in a temporary location |
| Pipeline | Connects the modules in the correct order |

We do not need to test every line individually. We test important behaviors, including:

* a normal case that should succeed;
* an invalid case that should raise an exception;
* a file-related case when appropriate.

## Test One Function at a Time

Keep each test focused. When a test fails, its name should identify the behavior being checked.

Clear names:

```python
test_validate_dataframe_removes_invalid_ratings
test_validate_dataframe_with_missing_column
test_save_data_creates_csv
test_remove_duplicates
test_handle_missing_rows
test_remove_outliers_iqr
...
```

Less helpful name:

```python
test_some_stuff
```

## Two types of test: unit test and integration test

A unit test focuses on one function or small component:

```text
validate_dataframe() receives a DataFrame → returns valid data
```

An integration test checks whether multiple parts work together:

```text
load data → validate data → process data → save output
```



---


# Part 2: `conftest.py` and `tmp_path`

## Share Fixtures with `conftest.py`

When multiple test files need the same setup, place the fixture in `tests/conftest.py`.

1. Open `tests/conftest.py` and create the fixture like below.

```python
# tests/conftest.py
from pathlib import Path
import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    """Read the existing MP1 sample CSV for each test."""
    filepath = Path("fixtures") / "sample_data.csv"
    return pd.read_csv(filepath)
```

pytest discovers `conftest.py` automatically, so test files do not import `sample_df`.

They request the fixture by name:

```python
def test_something(sample_df):
    assert len(sample_df) == 100
```

## Temporary Paths with `tmp_path`

We can also test whether output files are saved correctly. Tests should save generated files in a temporary directory rather than in the project repository.

pytest provides the built-in `tmp_path` fixture, which gives each test function its own temporary directory as a `Path` object. Again, we do not need to define or import this fixture.


```python
def test_temporary_path(tmp_path):
    output_path = tmp_path / "clean.csv"
```

---

# Try It Yourself — Add Tests to MP1

Apply the testing patterns to your MP1 functions. 


## 1. Add Validation Tests

Open `tests/test_data_validator.py` and copy and paste the starter code below.

Complete the TODOs below using function calls and `assert` statements:

```python
# tests/test_data_validator.py

import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    # TODO: Set the required and numeric column names.
    # TODO: Call validate_dataframe().
    # TODO: Assert that 98 rows remain and all five columns are preserved.
    pass


def test_validate_dataframe_with_missing_column(sample_df):
    # TODO: Set required_columns to include a nonexistent column.
    # TODO: Use pytest.raises(ValueError) around validate_dataframe().
    pass
```


## 2. Add a File-Output Test

Open `tests/test_data_output.py` and copy and paste the starter code below.

Complete the TODOs below using function calls and `assert` statements:

```python
#tests/test_data_output.py

import pandas as pd

from src import save_data


def test_save_data_creates_csv(sample_df, tmp_path):
    output_path = tmp_path / "clean.csv"

    # TODO: Call save_data() and store its return value.
    # TODO: Assert that the returned path is correct.
    # TODO: Read the saved CSV with pandas.
    # TODO: Assert that its row count and column names match sample_df.
    pass
```


## 3. Add Processing Tests

Open `tests/test_data_processor.py` and copy and paste the starter code below.

Complete the TODOs below using function calls and `assert` statements:

```python
#tests/test_data_processor.py

import pandas as pd
import pytest

from src.data_processor import handle_missing, remove_duplicates, remove_outliers


def test_remove_duplicates(sample_df):
    # TODO: Call remove_duplicates() on sample_df.
    # TODO: Assert that 98 rows remain.
    pass


def test_handle_missing_rows(sample_df):
    # Arrange: use the existing rating column.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce") 
    # note: errors="coerce" converts invalid numeric strings to missing values.

    # TODO: Call handle_missing() with axis="rows".
    # TODO: Assert that 97 rows remain.
    pass


def test_remove_outliers_iqr(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce") 
    df = df.dropna()
    # note: errors="coerce" converts invalid numeric strings to missing values.
    
    # TODO: Call remove_outliers() for ["rating"], using method="iqr", and threshold=1.5.
    # TODO: Assert that 95 rows remain.
    pass

# TODO: Use test_remove_outliers_iqr() as a reference to write test_remove_outliers_zscore(). Use the same numeric rating data without missing values, but set method="zscore" and threshold=3. Check the expected result for zscore and update your assertions accordingly.

# TODO: Use test_validate_dataframe_with_missing_column() as a reference to write test_remove_outliers_with_unsupported_method(). Use pytest.raises(ValueError) to confirm that remove_outliers() raises an error when called with method="unknown".
```


## 4. Run the Tests

```bash
python -m pytest -v
```

All eight tests should pass. If a test fails, read the failure message and check whether the issue is in the test or the application code.

## Save Your Work

```bash
git status
git add tests requirements.txt
git commit -m "Add pytest tests for MP1"
git push -u origin feature/pytest

git switch main
git pull origin main
git merge feature/pytest
git push origin main

git branch -d feature/pytest
git push origin --delete feature/pytest
```