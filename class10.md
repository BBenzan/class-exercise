# Weekly Announcements
* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
* **MP1** is completed! Great job! 
* **MP1 Check-off Meeting**
    * Rubric: https://docs.google.com/document/d/1tlLSdTx4zcqpXoM95dxW0EpbP9YjjwKP0w2CSXR0nb8. The link is also available on Canvas (Under main page, MP1 assignment)
    * Syllabus and Rubric: review both syllabus and rubric once again to understand what to expect.
    * Scheduling Reminder: Please make sure to schedule your meeting with your TA. One final follow-up email will be sent today, along with an announcement on Canvas. These will serve as the final reminders to schedule your check-off meeting. 


---

# Before We Begin

Open your `class-exercise` directory and activate its virtual environment.

Install pytest:

```bash
python -m pip install pytest
python -m pip freeze > requirements.txt
```

---

# Class 10: pytest Fundamentals and Fixtures

## Learning Objectives

By the end of today's class, you will be able to:

1. Explain why automated tests are useful.
2. Write and run a basic pytest test.
3. Organize a test using Arrange, Act, and Assert.
4. Test an expected exception with `pytest.raises()`.
5. Use a fixture to share test data.

> Complete all class exercises inside `class-exercise`. Make sure your virtual environment is active.

---

# Part 1: Why Write Tests?

Key: Instead of repeatedly checking our program ourselves, let automated tests check it for us.

We want to make sure our program behaves as expected. Without an automated test, we may repeatedly run a program and inspect the output ourselves. An automated test records the expected behavior and checks it consistently.

For example, after removing a duplicate row, we expect the number of rows to decrease while the columns remain unchanged. A test can check this for us. 

! Testing does not prove that a program has no bugs. It provides evidence that the situations we tested behave as expected.

---

# Part 2: Write and Run a Basic Test (quiz)

Pytest automatically discovers test files and test functions whose names begin with `test_`. So, we name our test files and functions with the `test_` prefix to let pytest find them automatically.

```python
#test_class10_pandas.py
import pandas as pd

def test_dataframe_shape():
    # This DataFrame has 5 rows and 4 columns.
    df = pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })

    # assert checks a condition. If it is true, the test continues. If it is false, the test fails.
    assert df.shape == (5, 4)
    # assert df.shape == (1, 1) 
    # ^ will get an AssertionError
```


Run the test:

```bash
python -m pytest -v test_class10_pandas.py
```

The result should include:

```text
test_dataframe_shape PASSED
```

Run all discovered tests from the current directory:

```bash
python -m pytest
```

Common results include:

* `PASSED`: the test completed successfully.
* `FAILED`: an assertion was false or an unexpected exception occurred during the test.
* `ERROR`: pytest encountered a problem during collection, setup, or teardown.

Try running the test with `assert df.shape == (1, 1)`.
---

## Arrange, Act, Assert 

A test can be organized into three parts:

1. **Arrange** — prepare the input and expected result.
2. **Act** — call the function being tested.
3. **Assert** — compare the actual behavior with the expected behavior.

Add this test to `test_class10_pandas.py`:

```python
#test_class10_pandas.py

def test_drop_duplicates():
    # Arrange
    df = pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })
    # note: the final two rows are identical, so removing duplicates leaves four rows and four columns.

    # Act
    result = df.drop_duplicates()

    # Assert
    assert result.shape == (4, 4)
    assert result["title"].tolist() == ["Movie A", "Movie B", "Movie C", "Movie D"]
```




---

# Part 3: Testing Expected Exceptions

An exception can be the expected result of a test.

`pytest.raises()` checks that a block of code raises the expected exception. For example, `float("unknown")` raises `ValueError`:

```python
import pytest

with pytest.raises(ValueError):
    float("unknown")
```

* If `ValueError` is raised, then the test passes -- pytest treats it as the expected result.
* If no exception is raised, or a different exception is raised, the test fails.

Unlike `try`/`except`, this is used to check that an error occurs, rather than to handle it and continue the program.

Let's use it inside a test. Add:

```python
#`test_class10_pandas.py`
import pytest 

def test_invalid_numeric_value():
    df = pd.DataFrame({"rating": [7, "unknown", 9]})

    with pytest.raises(ValueError):
        pd.to_numeric(df["rating"])
```

The test passes only if the code inside the `with` block raises `ValueError`. If no exception is raised, the test fails.

---

# Part 4: Fixtures

A fixture prepares data or another resource that a test needs. Fixtures reduce repeated setup code when multiple tests need the same data (i.e., we don't want to repeat "pd.DataFrame(...)")

We will use a Python decorator, `@pytest.fixture`, to define fixtures. For example,

```python
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })
```

Before creating a fixture, let’s briefly look at decorators.

## A quick note about Decorators

Simply put, decorators are a form of higher-order programming.

### Higher-order programming

The idea is that we treat functions just like regular variable (e.g., passing/returning a function into another function).

```python
# a simple function adding two number
def add(x,y): 
    return x + y

# a function adding 10 to a number 
def add_10(x): 
    return add(x,10)
# ^ an example of a higher-order function (it returns a function)
```

If we want to create a series of functions that add different constants, then we could do this:

```python
def add(x,y): 
    return x + y

def create_add_k(k):
    def _add_func(x):
        return add(x,k)
    return _add_func


add_10 = create_add_k(10)
add_5 = create_add_k(5)
add_1 = create_add_k(1)

# we could also use (*args, **kwargs) -- i.e., "since I don’t know how many arguments the function I’m wrapping will take, I’ll just accept whatever comes in and pass them right through!"

def create_add_k(k):
    def _add_func(*args, **kwargs):
        return add(*args, k, **kwargs)
    return _add_func

add_10 = create_add_k(10)
```

### Decorators

So, decorators are another example of higher-order programming. 

A decorator modifies or adds behavior to a function. 

Decorator example:

```python
# a simple function
def add(x, y): 
    return x + y

# a decorator 
def add_10(func):
    def wrapper(x,y): # (*args, **kwargs)
        return func(x,y) + 10 # (*args, **kwargs) + 10
    return wrapper

# Usecase: a decorator begins with `@` and appears immediately above a function.
@add_10
def add(x, y): 
    return x + y

print(add(2, 5))
```

### Pytest Decorator Example

```python
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })
```

`@pytest.fixture` tells pytest that `sample_df()` is a fixture. pytest can then call this function automatically and provide its returned value to a test that requests `sample_df`:


## Create a Fixture
And, add this fixture to `test_class10_pandas.py`:

```python
#test_class10_pandas.py

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })
```

Replace the two tests that create the same DataFrame with:

```python
def test_dataframe_shape(sample_df): # just sample_df instead of sample_df()
    assert sample_df.shape == (5, 4)

def test_drop_duplicates(sample_df):
    result = sample_df.drop_duplicates()
    assert result.shape == (4, 4)
    assert result["title"].tolist() == ["Movie A", "Movie B", "Movie C", "Movie D"]
```

- Request the fixture by using its name as a test-function parameter. 
- pytest calls the fixture and passes its returned value to the test. 
- By default, each test receives a newly created DataFrame.

---

# Part 5: Run and Read the Tests

Run:

```bash
python -m pytest -v test_class10_pandas.py
```

The result should include:

```text
test_invalid_numeric_value PASSED
test_dataframe_shape PASSED
test_drop_duplicates PASSED
```

To see a failure, temporarily change the expected shape from `(5, 4)` to `(4, 4)` in `test_dataframe_shape()` and run pytest again. Read the failure message, then restore the correct expectation.

The failure output should help answer:

* Which test failed?
* Which assertion failed?
* What was different between the expected and actual results?


# Part 6: Why Fixtures? (quiz)

We might ask: "What's the point of checking the sample data that we created?" It might seem redundant to check them. 

Here are the three key reasons why checking the shape in a fixture test is highly meaningful:

1. The Sanity Check: verifying your setup

- Make sure that functions work properly. Before you run complex logic or machine learning algorithms on your data, you must ensure your starting point is flawless.
    - If there is a typo in your fixture code, or if an automated data-loading step accidentally skips a row or column, this shape check will catch it instantly.
    - Without this, a broken fixture could cause your actual algorithm tests to fail. You would then waste hours debugging perfectly good code, only to realize the raw input data was corrupted.

- Make sure that the test can fail. 
    - The most dangerous test is one that passes no matter what.
    - By forcing a failure, you verify that your test assertions are actually wired correctly, that pytest is actively watching that variable, and that the failure messages are clear and readable.

2. Regression Testing: guarding against future changes

In real-world projects, shared fixtures are often modified by teammates or updated in future versions of the code.
- If a coworker adds a new feature column or removes an outdated row from the shared fixture, dozens of downstream tests might suddenly break without explanation.
- A dedicated shape test serves as a tripwire. It immediately points out: "Hey, someone altered the core sample data format!"

So, checking the dataframe shape isn't about testing your data's accuracy —- it is about proving that your test runner (pytest) and your test ingredients (fixtures) are calibrated before you start developing your real code.

---

# Try It Yourself — Test a Data Validator

Create these two files directly inside `class-exercise`:

* `class10_data_validator.py`
* `test_class10_data_validator.py`

The test filename begins with `test_` so pytest can discover it.

Copy the starter code below into the matching files, then complete TODOs 1–2. The validator is provided; your task is to write its tests.

## Starter Code

### `class10_data_validator.py`

```python
def validate_columns(df, required_columns):
    """Return the DataFrame if all required columns exist."""
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
        
    return df
```

### `test_class10_data_validator.py`

```python
import pandas as pd
import pytest

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
    # Act by calling validate_columns().
    # Assert that the returned DataFrame has the expected columns.
    pass


def test_validate_columns_with_missing_column(sample_df):
    # TODO 2:
    # Use pytest.raises() to confirm that validate_columns()
    # raises ValueError when a required column is missing.
    pass
```


## Requirements

Your tests should confirm that:

1. `validate_columns()` returns a DataFrame with the expected columns when all required columns exist.
2. `validate_columns()` raises `ValueError` when `rating` is required but missing.
3. The exception test checks that the message contains `Missing required columns`.
4. Both tests use the `sample_df` fixture.

Run:

```bash
python -m pytest -v test_class10_data_validator.py
```

Both tests should pass.

## Save Your Work

```bash
git status
git add test_class10_pandas.py class10_data_validator.py test_class10_data_validator.py requirements.txt
git commit -m "Add Class 10 pytest practice"
git push
```