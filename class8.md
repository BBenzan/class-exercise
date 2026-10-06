# Weekly Announcements

* **Office Hours Request Link:** https://forms.gle/cQStrQGdnsVZYPgT7
* **MP 1** is posted on Canvas under **Assignments**.
    * MP 1 - Parts 1-4 are available. 
* **MP1-WSU 4** is due on Friday (10/9) and will be available the night before.
* **MP1 Check-off Meeting**
    * Rubric: https://docs.google.com/document/d/1tlLSdTx4zcqpXoM95dxW0EpbP9YjjwKP0w2CSXR0nb8. The link is also available on Canvas (Under main page, MP1 assignment)
    * Email: You should have received, or will receive, an email from a TA by tonight. Please check your inbox and let me know if you haven’t received one by tomorrow.
    * Syllabus and Rubric: review both syllabus and rubric once again to understand what to expect.
* **Friday's class**: MP 1 Push Day! we will use the class time as an office-hour session. 

---

# Pre-lecture Try It Yourself

Before we begin the lecture, let's do a quick TIY to complete the code. 

We'll be using these materials for today’s topic.

## Create the Starter Project

Open your `class-exercise` directory:

```bash
cd class-exercise
```

Create these Python files in the same directory:

```text
class-exercise/
├── class8_pipeline.py
├── class8_data_loader.py
└── class8_data_validator.py
```

## Starter Code -- Complete the TODOs

### `class8_data_loader.py`

```python
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def load_netflix(filepath):
    """Load the Netflix CSV file."""
    # TODO 1:
    # Load filepath using pd.read_csv().
    # Log an INFO.
    # Return the DataFrame.
    pass
```

### `class8_data_validator.py`

```python
import logging

logger = logging.getLogger(__name__)

def require_columns(df, required_columns):
    """Check that all required columns exist."""
    # TODO 2:
    # Check if any of the configured columns (list) are missing from df.
    # If any are missing, log an ERROR and raise ValueError.
    # Log an INFO.
    # Return the DataFrame.
    pass
```

### `class8_pipeline.py`

```python
import logging
from pathlib import Path
from class8_data_loader import load_netflix
from class8_data_validator import require_columns

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    input_path = Path("data/messy_netflix_titles.csv")

    # TODO 3:
    # Inside a try/except block:
    # Load the data and require columns: ["title", "type", "release_year"].
    # Catch ValueError and exit with status code 1.
    # Log an INFO
    pass


if __name__ == "__main__":
    main()
```

Save the commpleted code.

```bash
git add class8_pipeline.py class8_data_loader.py class8_data_validator.py
git commit -m "Add Class 8 starter files"
```

---

# Class 8: Project Organization and Packages

## Learning Objectives

By the end of today's class, you will be able to:

1. Explain why a project is divided into directories and modules.
2. Describe the responsibility of each pipeline module.
3. Create package / `__init__.py` to expose selected functions.
4. Move tracked files while preserving Git history.
5. Update imports and file paths after reorganizing a project.

> Complete all class exercises inside `class-exercise`. Make sure your virtual environment is active.

---

# Part 1: Project Organization (quiz)

Our starter project places all files in one directory:

```text
class-exercise/
├── class8_pipeline.py
├── class8_data_loader.py
└── class8_data_validator.py
```

## Separation of Modules by Responsibility 

A pipeline often contains several responsibilities:

```text
Load → Validate → Process → Save
```

The main pipeline should coordinate these modules instead of containing every implementation detail.

Each responsibility can be placed in a separate module:

| Module | Responsibility |
| :--- | :--- |
| Data loader | Reads data from a file |
| Data validator | Checks whether the data is good to process |
| Data processor | Cleans or transforms the data |
| Data output | Saves the final result |
| Main pipeline | Coordinates all of the above |

## Organized Structure

This structure works for a small script.

```text
class-exercise/
├── class8_pipeline.py
├── class8_data_loader.py
└── class8_data_validator.py
```

As a project grows, however, it becomes harder to determine ...
- which files contain reusable code
- which file runs the program
- where the data belongs

A more organized structure:

```text
class-exercise/
├── class8_pipeline.py
└── class8_src/
    ├── __init__.py
    ├── class8_data_loader.py
    └── class8_data_validator.py
```

| Location | Purpose |
| :--- | :--- |
| `class8_pipeline.py` | Coordinates the steps and runs the program |
| `class8_src/` | Contains the functions/classes used by the program|

Project organization does not change what the program does. It changes where each responsibility belongs.

---


# Part 2: Packages and `__init__.py`

A directory containing `__init__.py`  is considered as a package. 

```text
src/
├── __init__.py
├── data_loader.py
└── data_validator.py
```

## Many Modules in a Package

Each module has functions, classes, and related logic.

```python
#src/data_loader.py
import pandas as pd
def load_data(filepath):
    return pd.read_csv(filepath)
```

```python
#src/data_validator.py
import pandas as pd
def check_data(data):
    return True
```

Can we import functions from multiple modules using a single import line?
- We can use `__init__.py` to provide a single entry point for functions and classes from different modules.

## Exposing Modules and Their Functions with `__init__.py`

Add selected functions to `src/__init__.py`:

```python
from .data_loader import load_data
from .data_validator import check_data
```

The dot means that the module is inside the current package.

The main script can then import directly from `src`:

```python
#main.py
from src import load_data, check_data
```

This creates a simpler public interface. The main file needs to know what the package provides, but it does not need to know where every function is implemented.


## Multiple Packages

```text
src/
├── data_processor/         # Package 1
│   ├── __init__.py
│   ├── data_loader.py
│   └── data_validator.py
└── app_api/                # Package 2
    ├── __init__.py
    └── routes.py
```

```python
from src.data_processor import load_data, check_data
```

---

# Try It Yourself — Reorganize the Starter Project 

Try completing this exercise as much as you can, and we will go through the solution together before class ends.

## If you finish early and feel confident about the exercise,

* Get checked off by either me or a TA.
* Once you have been checked off, you may leave.


Let's change the flat starter project into a package-based project.

## Step 1: Create the Directories

Run this command from inside `class-exercise`:

```bash
mkdir class8_src
```

Create an empty file named `__init__.py` inside `class8_src`.

## Step 2: Move the Tracked Files

Use `git mv`:

```bash
git mv class8_data_loader.py class8_src/class8_data_loader.py
git mv class8_data_validator.py class8_src/class8_data_validator.py
```

`git mv` moves the file and stages the change. Check the result:

```bash
git status
```

## Step 3: Update `class8_src/__init__.py`

```python
from .class8_data_loader import load_netflix
from .class8_data_validator import require_columns
```

## Step 4: Update the Pipeline Imports

In `class8_pipeline.py`, replace the original imports with:

```python
from class8_src import load_netflix, require_columns
```

The completed structure should be:

```text
class-exercise/
├── class8_pipeline.py
└── class8_src/
    ├── __init__.py
    ├── class8_data_loader.py
    └── class8_data_validator.py
```


## Run the Pipeline

```bash
python class8_pipeline.py
```

Your messages should identify the module that produced them:

```text
INFO     class8_src.class8_data_loader — Data loaded
INFO     class8_src.class8_data_validator — Validation completed
INFO     __main__ — Pipeline completed
```

## Save Your Work

```bash
git status
git add .
git commit -m "Organize Class 8 modules into a package"
git push
```
